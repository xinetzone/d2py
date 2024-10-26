import os
import sys
import pytest
import gymnasium as gym
import gym_multigrid

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

@pytest.mark.parametrize("env_id", ["gym_multigrid:multigrid-collect-v0"])
def test_collect_game(env_id) -> None:
    """Test collect_game()"""
    env = gym.make(env_id)

    obs, info = env.reset()
    while True:
        actions = [env.action_space.sample() for a in env.agents]
        obs, reward, terminated, truncated, info = env.step(actions)
        if terminated or truncated:
            print(f"episode ended after {env.step_count} steps")
            print(f"agents collected {env.collected_balls} objects")
            break
