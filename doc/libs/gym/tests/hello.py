import gymnasium as gym

# 初始化环境
# 创建名为 "LunarLander-v3" 的环境实例，并设置渲染模式为 "human"（即在窗口中显示环境）
env = gym.make("LunarLander-v3", render_mode="human") # 

# 重置环境以生成第一个观测值
observation, info = env.reset(seed=42)
for _ in range(1000):
    # 在这里插入你的策略
    action = env.action_space.sample() # 从动作空间中随机采样一个动作

    # 使用动作 action 通过环境进行转换
    # 接收下一个观测值、奖励以及该回合（episode）是否已结束或被截断（truncated）
    observation, reward, terminated, truncated, info = env.step(action)

    if terminated or truncated: # 如果回合结束，则可以重置以开始新的回合
        observation, info = env.reset()

env.close()
