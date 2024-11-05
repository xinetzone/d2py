from dataclasses import dataclass
from pathlib import Path
from typing import Any
import time
import logging
import numpy as np
import tensorflow as tf

from .utils import RunningStat, batch_iter
from .model import RewardPredictor, net_cnn

logger = logging.getLogger(f"drlhp.{__name__}")

@dataclass
class RewardPredictorEnsemble:
    core_network: RewardPredictor
    obs_shape: list[int]
    lr: float = 1e-4
    n_preds: int = 40
    log_dir: str = ".temp"

    def __post_init__(self):
        self.core_network = self.core_network(self.obs_shape)
        self.log_dir = Path(self.log_dir)
        self.rps = [
            RewardPredictor(self.core_network)
            for _ in range(self.n_preds)
        ]

    def raw_rewards(self, obs):
        """返回每个成员在单个片段中每一帧的（未标准化的）奖励。"""
        n_steps = obs.shape[0]
        for rp in self.rps:
            rp.trainable = False
            s1 = obs
            rs = rp.core_network(s1)
        rs = self.sess.run([rp.r1 for rp in self.rps], feed_dict)
        rs = np.array(rs)
        # Get rid of the extra x 1 dimension
        rs = rs[:, 0, :]
        np.testing.assert_equal(rs.shape, (self.n_preds, n_steps))
        return rs

    def reward(self, obs):
        """返回单个片段中每一帧（标准化后的）奖励。

        （标准化过程涉及分别对每个成员的奖励进行标准化，然后对所有成员的结果奖励求平均。）
        """
        n_steps = obs.shape[0]
        # 获取非标准化的奖励
        ensemble_rs = self.raw_rewards(obs)
        logger.debug(f"Unnormalized rewards:\n{ensemble_rs}", )
        # 标准化奖励
        # 请注意，在这里而不是在网络本身实现这一点，因为：
        # * 不在 TensorFlow 中做会更简单。
        # * 偏好预测不需要标准化的奖励。只有发送到 RL 算法的奖励需要被标准化。因此，可以节省计算资源。

        # 第4页：
        # “我们将 r^ 生成的奖励标准化为零均值和恒定的标准差。”
        # 第15页（Atari）：
        # “由于奖励预测器最终用于比较两个时间步长的和，其尺度是任意的，我们将其标准化为 0.05 的标准差。”
        # 第5页：
        # “估计值 r^ 是通过独立地对每个预测器进行标准化来定义的......”

        # 我们希望分别跟踪集合中每个成员的运行平均值/标准差，因此我们必须在这里谨慎一些。
        np.testing.assert_equal(ensemble_rs.shape, (self.n_preds, n_steps))
        ensemble_rs = ensemble_rs.transpose()
        np.testing.assert_equal(ensemble_rs.shape, (n_steps, self.n_preds))
        for ensemble_rs_step in ensemble_rs:
            self.r_norm.push(ensemble_rs_step)
        ensemble_rs -= self.r_norm.mean
        ensemble_rs /= (self.r_norm.std + 1e-12)
        ensemble_rs *= 0.05
        ensemble_rs = ensemble_rs.transpose()
        np.testing.assert_equal(ensemble_rs.shape, (self.n_preds, n_steps))
        logger.debug(f"Reward mean/stddev:\n{self.r_norm.mean} {self.r_norm.std}")
        logger.debug(f"Normalized rewards:\n{ensemble_rs}", )

        # “...然后对结果进行平均。”
        rs = np.mean(ensemble_rs, axis=0)
        np.testing.assert_equal(rs.shape, (n_steps, ))
        logger.debug(f"After ensemble averaging:\n{rs}", ) 
        return rs
    