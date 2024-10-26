import logging
import gymnasium as gym
from drlhp import HumanPreferencesEnvWrapper
from easy_log import config_logging

logger = logging.getLogger("drlhp")

config_logging('compile.log', "drlhp", maxBytes=5000000, backupCount=7)

# 初始化环境
# 创建名为 "LunarLander-v3" 的环境实例，并设置渲染模式为 "human"（即在窗口中显示环境）
env = gym.make("LunarLander-v2", render_mode="human") 
# env = gym.make('multigrid-collect-v0', render_mode="human")

wrapped_env = HumanPreferencesEnvWrapper(env, 
                                         segment_length=100,
                                         n_initial_training_steps=10)

# 重置环境以生成第一个观测值
# observation, info = env.reset(seed=42)
wrapped_env.reset()
for _ in range(2):
    # wrapped_env.render
    # 在这里插入你的策略
    # nb_agents = len(wrapped_env.agents)
    action = wrapped_env.action_space.sample() # 从动作空间中随机采样一个动作
    # ac = [wrapped_env.action_space.sample() for _ in range(nb_agents)]

    # 使用动作 action 通过环境进行转换
    # # 接收下一个观测值、奖励以及该回合（episode）是否已结束或被截断（truncated）
    wrapped_env.step(action)
    # logger.info(info)
    # observation, reward, done, info = wrapped_env.step(action)

    # if done: # 如果回合结束，则可以重置以开始新的回合
    #     observation, info = wrapped_env.reset()

wrapped_env.close()
