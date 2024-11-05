from dataclasses import dataclass
from pathlib import Path
import logging
import queue
from typing import Any, SupportsFloat, Callable
import multiprocessing as mp
import numpy as np
from gymnasium import Wrapper, Env
import gymnasium as gym
from gymnasium import Wrapper, Env
from gymnasium.core import WrapperActType, WrapperObsType, RenderFrame, ObsType, ActType
from gym_multigrid.core.constants import TILE_PIXELS
from .config import _run_pref_interface, _train_reward_predictor
from .pref_db import Segment, PrefDB, PrefBuffer
from .pref_interface import PrefInterface
from .reward_predictor import RewardPredictorEnsemble

logger = logging.getLogger(f"drlhp.{__name__}")

@dataclass
class HumanPreferencesEnvWrapper(Wrapper):
    env: Env[ObsType, ActType]
    reward_predictor_network: Callable #= net_cnn,
    train_reward: bool = True
    collect_prefs: bool = True
    segment_length: int = 40
    mp_context: str = 'spawn'
    prefs_dir: str = None
    max_prefs_in_db: int = 10000
    obs_transform_func: Callable = None
    n_initial_training_steps: int = 50
    n_initial_prefs: int = 40
    pretrained_reward_predictor_dir: str = None
    reward_predictor_ckpt_interval: int = 10
    reward_predictor_refresh_interval: int = 10
    val_interval: int = 10
    reward_database_refresh_interval: int = 1
    synthetic_prefs: bool = True
    max_pref_interface_segs: int = 25
    zoom_ratio: int = 4
    channels: int = 3
    env_wrapper_log_level: int = logging.INFO
    reward_predictor_log_level: int = logging.INFO
    pref_interface_log_level: int = logging.INFO
    log_dir: str = ".temp"

    def __post_init__(self):
        self.log_dir = Path(self.log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        # self.metadata = {"render_modes": ["human", "rgb_array"], "render_fps": 4}
        self.obs_shape = self.env.observation_space.shape
        # self.reward_predictor_network = self.reward_predictor_network(self.obs_shape)
        logger.info(self.reward_predictor_network)
        self.preference_interface = PrefInterface(synthetic_prefs=self.synthetic_prefs,
                                                  max_segs=self.max_pref_interface_segs,
                                                  channels=self.channels,
                                                  zoom=self.zoom_ratio)
        # 将一堆初始化参数保存为包装属性。
        self.max_prefs = self.max_prefs_in_db
        self.ckpt_interval = self.reward_predictor_ckpt_interval

        # 将计数器和状态变量设置为初始值。
        self.segments_collected = 0
        self.reward_predictor_n_train = 0
        self.using_reward_from_predictor = False
        self.force_return_true_reward = False
        self.collecting_segments = True
        self.last_true_reward = None

        # 创建空的观测堆栈和新的片段
        self.recent_obs_stack = []
        self.episode_segment = Segment()
        self.reward_predictor_checkpoint_dir = self.log_dir/'reward_predictor_checkpoints'

        # 创建用于处理多进程通信的队列和共享值
        # TODO: 弄清楚如何使这些机制与更大的队列一起工作，以便我们不会因为时间问题而丢弃片段
        self.seg_pipe = mp.get_context(self.mp_context).Queue(maxsize=5)
        self.pref_pipe = mp.get_context(self.mp_context).Queue(maxsize=1)
        self.pref_db_size = mp.get_context(self.mp_context).Value('i', 0)
        self.kill_pref_interface_flag = mp.get_context(self.mp_context).Value('i', 0)
        self.kill_reward_training_flag = mp.get_context(self.mp_context).Value('i', 0)
        self.save_model_flag = mp.get_context(self.mp_context).Value('i', 0)
        self.save_prefs_flag = mp.get_context(self.mp_context).Value('i', 0)
        self.reward_training_steps = mp.get_context(self.mp_context).Value('i', 0)

        # 为以后初始化的内容创建占位参数
        self.pref_interface_proc = None
        self.reward_training_proc = None
        self.pref_buffer = None
        self.reward_predictor = None

        # 如果我们想收集偏好设置，我们需要启动运行 PrefInterface 的进程。
        if self.collect_prefs:
            self._start_pref_interface()
        # 如果我们想保存偏好设置和/或训练奖励模型，
        # 需要启动奖励预测器训练进程（该进程还负责创建用于存储/保存偏好设置的PrefDB）
        if self.train_reward or self.collect_prefs:
            self._start_reward_predictor_training()

    
    def _start_pref_interface(self):
        self.pref_interface_proc = mp.get_context(self.mp_context).Process(target=_run_pref_interface, daemon=True,
                                                                           args=(self.preference_interface,
                                                                                 self.seg_pipe,
                                                                                 self.pref_pipe,
                                                                                 self.kill_pref_interface_flag,
                                                                                 self.pref_interface_log_level))
        self.pref_interface_proc.start()

    def _start_reward_predictor_training(self):
        self.reward_training_proc = mp.get_context(self.mp_context).Process(target=_train_reward_predictor, daemon=True,
                                                                    args=(self.reward_predictor_network,
                                                                          self.train_reward,
                                                                          self.pretrained_reward_predictor_dir,
                                                                          self.obs_shape,
                                                                          self.pref_pipe,
                                                                          self.pref_db_size,
                                                                          self.prefs_dir,
                                                                          self.max_prefs,
                                                                          self.ckpt_interval,
                                                                          self.n_initial_prefs,
                                                                          self.reward_training_steps,
                                                                          self.reward_database_refresh_interval,
                                                                          self.val_interval,
                                                                          self.kill_reward_training_flag,
                                                                          self.save_prefs_flag,
                                                                          self.save_model_flag,
                                                                          self.log_dir,
                                                                          self.reward_predictor_log_level))
        self.reward_training_proc.start()

    def _update_episode_segment(self, obs, reward, terminated, truncated):
        """从最近的环境 step 中获取观测值并将其添加到现有分段中。
        如果分段达到了所需长度，则将其完成并通过 `seg_pipe` 发送给 `PrefInterface`

        :param obs: 来自底层环境的（可能是堆叠的）观测值
        :param reward: 底层环境的奖励（用于合成偏好设置）
        :param terminated, truncated: 是否终止了该回合，如果是，应该填充分段的其余部分然后开始新的分段
        :return:
        """
        if self.obs_transform_func is not None:
            obs = self.obs_transform_func(obs)
        self.episode_segment.append(np.copy(obs), np.copy(reward))
        if terminated or truncated:
            while len(self.episode_segment) < self.segment_length:
                self.episode_segment.append(np.copy(obs), 0)

        if len(self.episode_segment) == self.segment_length:
            self.segments_collected += 1
            self.episode_segment.finalise()
            try:
                self.seg_pipe.put(self.episode_segment, block=False)
            except queue.Full:
                # If the preference interface has a backlog of segments
                # to deal with, don't stop training the agents. Just drop
                # the segment and keep on going.
                pass
            self.episode_segment = Segment()

    def save_prefs(self):
        self.save_prefs_flag.value = 1

    def save_reward_predictor(self):
        self.save_model_flag.value = 1

    def stop_segment_collection(self):
        self.collecting_segments = False

    def start_segment_collection(self):
        self.collecting_segments = True
        self.episode_segment = Segment()

    def _load_reward_predictor(self, model_load_dir):
        if self.reward_predictor is None:
            logger.info(f"Loading reward predictor from {model_load_dir}; will use its model reward now")
            self.reward_predictor = RewardPredictorEnsemble(
                core_network=self.reward_predictor_network,
                log_dir=self.log_dir,
                lr=7e-4,
                obs_shape=self.obs_shape,
                logger=logger)
        self.reward_predictor_n_train = self.reward_training_steps.value

    def step(self, action):
        # 检查是否恰好达到模型训练足够步数的点
        minimum_training_steps_reached = self.reward_training_steps.value >= self.n_initial_training_steps
        sufficiently_trained = self.reward_predictor is None and minimum_training_steps_reached
        # 检查是否存在尚未加载的现有预训练模型。
        pretrained_model = self.reward_predictor is None and self.pretrained_reward_predictor_dir is not None
        # 检查是否应该用新的奖励预测器来更新现有的奖励预测器，因为自上次更新以来已经完成了足够的训练步骤。
        should_update_model = minimum_training_steps_reached and (self.reward_training_steps.value - self.reward_predictor_n_train > self.reward_predictor_refresh_interval)
        logger.info(f"reward_training_steps.value: {self.reward_training_steps.value}, reward_predictor: {self.reward_predictor}")
        logger.info(f"should_update_model: {should_update_model}, sufficiently_trained: {sufficiently_trained}, pretrained_model:{pretrained_model}")
        # 如果其中任何一个条件为真，就加载模型
        if sufficiently_trained or pretrained_model or should_update_model:
            if sufficiently_trained:
                logger.info("Model is sufficiently trained, switching to it for reward")
                model_load_dir = self.reward_predictor_checkpoint_dir
            elif should_update_model:
                logger.info("Updating model used for env reward")
                model_load_dir = self.reward_predictor_checkpoint_dir
            else:
                model_load_dir = self.pretrained_reward_predictor_dir
                logger.info("Loading pretrained model for env reward")
            self._load_reward_predictor(model_load_dir)
            self.using_reward_from_predictor = True
        obs, reward, terminated, truncated, info = self.env.step(action)
        logger.debug(f"obs, reward, terminated, truncated, info: {obs.shape, reward, terminated, truncated, info}")

        if self.collecting_segments:
            self._update_episode_segment(obs, reward, terminated, truncated)
        logger.info(obs.shape)
        if self.reward_predictor is not None and not self.force_return_true_reward:
            # 如果我们设置了 self.force_return_true_reward，环境将返回真实的底层奖励（用于评估目的）。
            predicted_reward = self.reward_predictor.reward(np.array([np.array(obs)]))[0]
            self.last_true_reward = reward
            return obs, predicted_reward, terminated, truncated, info
        else:
            return obs, reward, terminated, truncated, info

    def switch_to_true_reward(self):
        if not self.using_reward_from_predictor:
            raise Warning("Environment has no reward predictor loaded, and is thus returning true reward")
        elif self.force_return_true_reward:
            raise Warning("Environment already returning true reward, no change")
        else:
            self.using_reward_from_predictor = False
            self.force_return_true_reward = True

    def switch_to_predicted_reward(self):
        """
        Note: this only works to undo a prior forcing of true reward
        if a reward model is already loaded, it can't cause a reward model to exist if it isn't present
        """
        if not self.force_return_true_reward:
            raise Warning("Environment already returning predicted reward, no change")
        else:
            self.using_reward_from_predictor = True
            self.force_return_true_reward = False

    def _cleanup_processes(self):
        logger.debug("Sending kill flags to processes")
        self.kill_reward_training_flag.value = 1
        self.kill_pref_interface_flag.value = 1

        logger.debug("Joining processes that are running")
        if self.reward_training_proc is not None:
            self.reward_training_proc.join()
        if self.pref_interface_proc is not None:
            self.pref_interface_proc.join()

        logger.debug("Closing seg pipe")
        self.seg_pipe.close()
        self.seg_pipe.join_thread()
        logger.debug("Closing pref pipe")
        self.pref_pipe.close()
        self.pref_pipe.join_thread()

    def close(self):
        logger.debug("env.close() was called")
        self._cleanup_processes()
        self.env.close()

