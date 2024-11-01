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

    """
    Basically a large lambda function for calling pref_interface.run(); meant to be used as the target of a
    multiprocessing Process.

    :param pref_interface: The PrefInterface object you want to run
    :param seg_pipe: A multiprocessing Queue in which the env will add new segments for the PrefInterface to pair and
                     request preferences for
    :param pref_pipe: A multiprocessing Queue for the PrefInterface to add preferences once collected, which will make
                      them accessible to the PrefDB in which they are stored and used for reward predictor training
    :param remaining_pairs: A multiprocessing Value that the PrefInterface can use to keep track of the remaining pairs
                            of segments it has to get preferences for, so that information is accessible externally
    :param kill_processes: A multiprocessing Value that will be set to 1 if we want to terminate running processes
                           (specifically, it will trigger pref_interface.run() to return so we can easily join
                           the process)
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
    print("RewardPredictorEnsemble created")
    # reward_predictor.init_network(load_ckpt_dir=checkpoint_dir)
    # print("RewardPredictorEnsemble initialized")
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
    A function, meant to be run inside a multiprocessing process, to create training and validation PrefDBs, and
    train a reward predictor using the preferences stored in those DBs.


    :param reward_predictor_network: A callable mapping from input obs to reward scalar
    :param obs_shape: A tuple specifying the input observation shape you want your reward model to take in
    :param pref_pipe: A multiprocessing queue for the PrefInterface to send segment pairs with preferences attached to
                      them to the PrefBuffer
    :param reward_training_steps: A multiprocessing value for keeping track of reward training steps
    :param prefs_dir: A string path specifying where existing preference DBs are stored on disk; if None, new
                      empty PrefDBs are created
    :param max_prefs: The max number of preferences to store in your PrefDBs, across both training and validation
    :param ckpt_interval: The interval of reward training steps on which to save a checkpoint of our reward predictor
    :param kill_processes_flag: A multiprocessing Value that will be set to 1 when we want to terminate processes;
                                this will trigger this function to return, making it easier to join the process
    :param database_refresh_interval: The interval of reward training steps on which to update the PrefDBs being used
                                      to train our reward predictor
    :param validation_interval: The interval of reward training steps on which to perform validation of the reward model
    :param num_initial_prefs: How many preferences our training PrefDB must have before we start training
                              the reward model
    :param save_prefs_flag: A multiprocessing Value that will be set to 1 when we want to save preferences
    :param save_model_flag: A multiprocessing Value that will be set to 1 when we want to trigger a model save
    :param pretrained_reward_predictor_dir: A string path specifying where a pre-trained reward model is saved;
                                            if None, assumes none exist, and initializes reward model from random
    :param log_dir: A strong path specifying a directory where logs and artifacts will be saved
    :param log_level: The log level you want for the logger within this function
    :param train_reward: A boolean specifying whether you want to actually train a reward model, or just use this
                         function to create a set of PrefDBs so they can be filled with preferences.
    :param pref_db_size: A multiprocessing Value used to store the aggregated size of our PrefDBs, so that size can be
                         queried externally
    """

    reward_predictor_logger = logging.getLogger("drlhp._train_reward_predictor")
    reward_predictor_logger.setLevel(log_level)
    reward_predictor_logger.info("Process for PrefDB and Reward Predictor started")
    # 使用指定的核心网络和观察形状创建 RewardPredictorEnsemble
    reward_predictor = _make_reward_predictor(reward_predictor_network,
                                              log_dir,
                                              obs_shape,
                                              checkpoint_dir=pretrained_reward_predictor_dir)
    # Create a PrefBuffer that receives preferences from the PrefInterfaces and store them in PrefDBs
    pref_buffer = _load_or_create_pref_db(prefs_dir, max_prefs, reward_predictor_logger)
    pref_buffer.start_recv_thread(pref_pipe)
    minimum_prefs_met = False

    while 1:
        pref_db_train, pref_db_val = pref_buffer.get_dbs()
        current_train_size = len(pref_db_train)
        current_val_size = len(pref_db_val)
        pref_db_size.value = current_train_size + current_val_size

        # If there has been an external trigger telling us to save preferences, do so, then reset it to 0 so we
        # won't save on subsequent iterations unless the flag is set again
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

