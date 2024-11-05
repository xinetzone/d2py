# -*- coding: UTF-8 -*-

import argparse
import random
import numpy as np
import torch
import gymnasium as gym
# import pybullet_envs
# import matplotlib.pyplot as plt

# model
from model.ppo import PPO
from config import get_config
# wrappers
from human_feedback_wrapper import HumanFeedback, SyntheticFeedback
from reward_wrapper import FeedbackReward


parser = argparse.ArgumentParser()
parser.add_argument(
    "--env-name", required=True, type=str, choices=["cartpole", "pendulum", "cheetah"]
)
parser.add_argument("--synthetic", dest="synthetic", action="store_true")
parser.add_argument("--seed", type=int, default=1)
parser.add_argument("--entropy", type=float, choices=[0.0, 0.01, 0.05, 0.1], default=0.1)
parser.add_argument("--constant-ask", type=int, choices=[100, 1000, 10000], default=1000)
parser.add_argument("--collect-initial", type=int, choices=[0, 50, 200], default=0)
parser.add_argument("--num-batches", type=int, default=100)
parser.set_defaults(use_baseline=True)


if __name__ == "__main__":

    args = parser.parse_args()

    torch.random.manual_seed(args.seed)
    np.random.seed(args.seed)
    random.seed(args.seed)

    config = get_config(args.env_name, args.seed, args.entropy, args.constant_ask, args.collect_initial, args.num_batches)
    
    if args.synthetic:
        env = SyntheticFeedback(FeedbackReward(gym.make(config.env_name)), config=config)
    else:
        env = HumanFeedback(FeedbackReward(gym.make(config.env_name)), config=config)
    eval_env = gym.make(config.env_name)
    
    # train model
    observation = eval_env.reset()
    eval_env.reset()
    model = PPO(env, eval_env, config, args.seed)
    model.train()
    print ("{} preference collected total".format(env.pref_db.total_labeled))
    
    # display final agent behavior 
    total_reward = 0
    done = False 
    eval_env.reset()

    while not done:
        eval_env.render(mode = "human")
        observation, reward, done, info = eval_env.step(model.policy.act(observation))
        total_reward += reward

    eval_env.close()
    print("total reward = ", total_reward)

