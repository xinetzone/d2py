import multiprocessing as mp
# from gymnasium import Wrapper, Env
import numpy as np
import os
import time
import os.path as osp
import queue
import logging
from .pref_db import Segment, PrefDB, PrefBuffer
from .pref_interface import PrefInterface
from .reward_predictor import RewardPredictorEnsemble
# from .reward_predictor_core_network import net_cnn
from typing import Callable

logger = logging.getLogger(f"drlhp.{__name__}")

PREFS_VAL_FRACTION = 0.2


def _save_prefs(pref_buffer: PrefBuffer,
                log_dir: str,
                logger: logging.Logger):
    """
    Saves the preferences stored in the databases on a given PrefBuffer to directories within `log_dir`

    :param pref_buffer: The PrefBuffer containing train and validation DBs we want to save
    :param log_dir: The directory to which we want our `train|val.pkl.gz` files to be saved
    :param logger: The logger object we want to use to log progress within this function
    """
    pref_db_train, pref_db_val = pref_buffer.get_dbs()
    train_path = osp.join(log_dir, 'train.pkl.gz')
    pref_db_train.save(train_path)
    logger.info(f"Saved {len(pref_db_train)} training preferences to '{train_path}'")
    val_path = osp.join(log_dir, 'val.pkl.gz')
    pref_db_val.save(val_path)
    logger.info(f"Saved {len(pref_db_val)} validation preferences to '{val_path}'")


def _load_or_create_pref_db(prefs_dir: str,
                            max_prefs: int,
                            logger: logging.Logger) -> PrefBuffer:
    """
    Create a PrefBuffer containing of two PrefDBs, either by loading them from disk (if `prefs_dir` is not None)
    or creating them from scratch.

    :param prefs_dir: Directory which PrefDBs should be loaded from; if None, they should be created anew
    :param max_prefs: The total number of preferences we want to store in the PrefDBs (split across both train and val DBs)
    :param logger: The logger object we want to use to log progress within this function

    :return: A PrefBuffer containing your PrefDBs
    """

    if prefs_dir is not None:
        train_path = osp.join(prefs_dir, 'train.pkl.gz')
        pref_db_train = PrefDB.load(train_path)
        logger.info("Loaded training preferences from '{}'".format(train_path))
        n_prefs, n_segs = len(pref_db_train), len(pref_db_train.segments)
        logger.info("({} preferences, {} segments)".format(n_prefs, n_segs))

        val_path = osp.join(prefs_dir, 'val.pkl.gz')
        pref_db_val = PrefDB.load(val_path)
        logger.info("Loaded validation preferences from '{}'".format(val_path))
        n_prefs, n_segs = len(pref_db_val), len(pref_db_val.segments)
        logger.info("({} preferences, {} segments)".format(n_prefs, n_segs))
    else:
        n_train = max_prefs * (1 - PREFS_VAL_FRACTION)
        n_val = max_prefs * PREFS_VAL_FRACTION
        pref_db_train = PrefDB(maxlen=n_train)
        pref_db_val = PrefDB(maxlen=n_val)
    pref_buffer = PrefBuffer(db_train=pref_db_train,
                             db_val=pref_db_val)
    return pref_buffer

def _run_pref_interface(pref_interface: PrefInterface,
                        seg_pipe: mp.Queue,
                        pref_pipe: mp.Queue,
                        kill_processes: mp.Value,
                        log_level: int = logging.INFO):
    """
    基本上这是一个大型lambda函数，用于调用pref_interface.run()；旨在用作多进程Process的 target。

    :param pref_interface: 你想要运行的PrefInterface对象
    :param seg_pipe: 一个多进程Queue，env会在其中添加新的分段供PrefInterface进行配对并请求偏好设置
    :param pref_pipe: 一个多进程Queue，PrefInterface在收集到偏好设置后将其加入其中，这将使这些偏好设置可被存储和用于奖励预测器训练的PrefDB访问
    :param remaining_pairs: 一个多进程Value，PrefInterface可以使用它来跟踪剩余的分段对，以便外部可以访问这些信息
    :param kill_processes: 一个多进程Value，如果我们想要终止正在运行的进程（特别是，它将触发pref_interface.run()返回，这样我们可以方便地加入进程），这个值将被设置为1
    """
    pref_interface.run(seg_pipe=seg_pipe,
                       pref_pipe=pref_pipe,
                       kill_processes=kill_processes,
                       log_level=log_level)
    
def _make_reward_predictor(reward_predictor_network: Callable,
                           log_dir: str,
                           obs_shape: tuple,
                           checkpoint_dir: str = None) -> RewardPredictorEnsemble:
    """辅助函数，用于创建 RewardPredictorEnsemble 并在存在检查点的情况下使用它进行初始化。
    
    如果 `checkpoint_dir` 为 `None`，奖励预测器将随机初始化。

    参数:
    - `reward_predictor_network`: 可调用的 Tensorflow 训练模型，接受观察结果并输出奖励
    - `log_dir`: 字符串路径，指定你希望 `RewardPredictorEnsemble` 存储日志和其他工件的位置
    - `obs_shape`: 元组，指定你希望你的 `RewardPredictorEnsemble` 接收的观察形状
    - `logger`: 希望在这个函数中使用来记录进度的日志对象
    - `checkpoint_dir`: 可选，字符串路径，指定你想要从中加载已保存的 RewardPredictorEnsemble 的检查点目录

    返回值:
    - 你新创建的 `RewardPredictorEnsemble`
    """
    log_dir: str = ".temp"
    reward_predictor = RewardPredictorEnsemble(
        core_network=reward_predictor_network,
        obs_shape=obs_shape,
        lr=7e-4,
        n_preds=40,
        log_dir=log_dir,)
    logger.info("RewardPredictorEnsemble created")
    return reward_predictor


def _train_reward_predictor(reward_predictor_network: Callable,
                            train_reward: bool,
                            pretrained_reward_predictor_dir: str,
                            obs_shape: tuple,
                            pref_pipe: mp.Queue,
                            pref_db_size: int,
                            prefs_dir: str,
                            max_prefs: int,
                            ckpt_interval: int,
                            num_initial_prefs: int,
                            reward_training_steps: mp.Value,
                            database_refresh_interval: int,
                            validation_interval: int,
                            kill_processes_flag: mp.Value,
                            save_prefs_flag: mp.Value,
                            save_model_flag: mp.Value,
                            log_dir: str,
                            log_level: int # logging levels are technically ints
                            ):
    """
    一个函数，旨在在多进程处理中运行，以创建训练和验证 PrefDBs，并使用存储在这些数据库中的偏好来训练奖励预测器。

    :param reward_predictor_network: 一个可调用的映射，从输入观测到奖励标量
    :param obs_shape: 一个元组，指定您希望奖励模型接受的输入观测形状
    :param pref_pipe: 一个多进程队列，用于PrefInterface发送带有偏好的片段对给PrefBuffer
    :param reward_training_steps: 一个多进程值，用于跟踪奖励训练步骤
    :param prefs_dir: 一个字符串路径，指定现有偏好数据库在磁盘上的存储位置；如果为None，则创建新的空PrefDBs
    :param max_prefs: 在您的PrefDBs中存储的最大偏好数量，涵盖训练和验证
    :param ckpt_interval: 保存奖励预测器检查点的奖励训练步长间隔
    :param kill_processes_flag: 一个多进程值，当想要终止进程时将设置为1；这将触发此函数返回，使得更容易加入进程
    :param database_refresh_interval: 更新用于训练奖励预测器的PrefDBs的奖励训练步长间隔
    :param validation_interval: 执行奖励模型验证的奖励训练步长间隔
    :param num_initial_prefs: 我们的培训PrefDB必须有多少偏好，我们才能开始训练奖励模型
    :param save_prefs_flag: 一个多进程值，当想要保存偏好时将设置为1
    :param save_model_flag: 一个多进程值，当想要触发模型保存时将设置为1
    :param pretrained_reward_predictor_dir: 一个字符串路径，指定预训练奖励模型的保存位置；如果为None，假设不存在，并从随机初始化奖励模型
    :param log_dir: 一个强路径，指定日志和工件将被保存的目录
    :param log_level: 此函数内记录器的日志级别
    :param train_reward: 一个布尔值，指定您是否真的想训练一个奖励模型，或者只是使用这个函数来创建一组PrefDBs，以便它们可以被填充偏好。
    :param pref_db_size: 一个多进程值，用于存储我们的PrefDBs的聚合大小，以便可以从外部查询大小
    """
    reward_predictor_logger = logging.getLogger("drlhp._train_reward_predictor")
    reward_predictor_logger.setLevel(log_level)
    reward_predictor_logger.info("Process for PrefDB and Reward Predictor started")
    # 使用指定的核心网络和观察形状创建 RewardPredictorEnsemble
    reward_predictor = _make_reward_predictor(reward_predictor_network,
                                              log_dir,
                                              obs_shape,
                                              checkpoint_dir=pretrained_reward_predictor_dir)
    # 创建 PrefBuffer，它从 PrefInterfaces 接收偏好并将它们存储在 PrefDBs 中
    pref_buffer = _load_or_create_pref_db(prefs_dir, max_prefs, reward_predictor_logger)
    pref_buffer.start_recv_thread(pref_pipe)
    minimum_prefs_met = False

    while 1:
        pref_db_train, pref_db_val = pref_buffer.get_dbs()
        current_train_size = len(pref_db_train)
        current_val_size = len(pref_db_val)
        pref_db_size.value = current_train_size + current_val_size
        # 如果有外部触发告诉我们要保存偏好，请这样做，然后将其重置为 0，这样我们就不会在后续迭代中再次保存，除非该标志再次被设置。
        if save_prefs_flag.value == 1:
            _save_prefs(pref_buffer, log_dir, reward_predictor_logger)
            save_prefs_flag.value = 0

        # If there's been an external trigger telling this process to die, stop the receiving thread on the PrefBuffer,
        # and then return from the function
        if kill_processes_flag.value == 1:
            pref_buffer.stop_recv_thread()
            return
        if not train_reward:
            # There might be some circumstances where we just want to collect and save preferences (for which we need
            # to create a PrefDB using this function) but might not want to actually train a reward model.
            continue

        if not minimum_prefs_met:
            # Confirm that we have at least `num_initial_prefs` training examples, and 1 validation example
            if current_train_size < num_initial_prefs or current_val_size < 1:
                reward_predictor_logger.debug(f"Reward dbs of length ({len(pref_db_train)}, {len(pref_db_val)}), waiting for minimum length ({num_initial_prefs}, 1) to start training")
                time.sleep(1)
                continue
            else:
                minimum_prefs_met = True
        if reward_training_steps.value % database_refresh_interval == 0:
            pref_db_train, pref_db_val = pref_buffer.get_dbs()

        reward_predictor_logger.info(f"Training reward predictor on {current_train_size} preferences, testing on {current_val_size}, iteration {reward_training_steps.value }")
        reward_predictor.train(pref_db_train, pref_db_val, validation_interval)
        reward_training_steps.value += 1
        if (save_model_flag.value == 1) or (reward_training_steps.value % ckpt_interval == 0):
            _save_prefs(pref_buffer, log_dir, reward_predictor_logger)
            reward_predictor.save()
            save_model_flag.value = 0

