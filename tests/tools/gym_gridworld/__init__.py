""""
参考 https://gymnasium.farama.org/tutorials/gymnasium_basics/environment_creation/，
代码示例
"""
from gymnasium.envs.registration import register

register(
    id="gym_gridworld/GridWorld-v0",
    entry_point="gym_gridworld.envs:GridWorldEnv",
)
