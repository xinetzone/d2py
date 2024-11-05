# import torch.nn as nn
from datetime import datetime

class config_cartpole:
    def __init__(self, use_baseline, ppo, seed, num_batches):
        self.env_name = "CartPoleBulletEnv-v1"
        self.record = False
        baseline_str = ("baseline" if use_baseline else "no_baseline") if not ppo else "ppo"
        seed_str = "seed=" + str(seed)
        # output config
        self.output_path = "results/{}-{}-{}/".format(
            self.env_name, baseline_str, seed_str
        )
        self.model_output = self.output_path + "model.weights/"
        self.log_path = self.output_path + "log.txt"
        self.scores_output = self.output_path + "scores.npy"
        self.plot_output = self.output_path + "scores.png"
        self.record_path = self.output_path
        self.record_freq = 5
        self.summary_freq = 1

        # model and training config
        self.num_batches = num_batches # number of batches trained on
        self.batch_size = 2000  # number of steps used to compute each policy update
        self.max_ep_len = 200  # maximum episode length
        self.learning_rate = 3e-2
        self.gamma = 1.0  # the discount factor
        self.use_baseline = use_baseline
        self.normalize_advantage = True

        # parameters for the policy and baseline models
        self.n_layers = 1
        self.layer_size = 64

        # hyperparameters for PPO
        self.eps_clip = 0.2
        self.update_freq = 5

        # since we start new episodes for each batch
        assert self.max_ep_len <= self.batch_size
        if self.max_ep_len < 0:
            self.max_ep_len = self.batch_size


class config_pendulum:
    def __init__(self, seed, entropy = 0.1, constant_ask_frequency = 1000, collect_initial = 0, num_batches=100):

        current_time = datetime.now().strftime("%H%M%S")

        # self.env_name = "InvertedPendulumBulletEnv-v0"
        self.env_name = "Pendulum-v1"
        self.record = True
        self.entropy = entropy
        seed_str = "seed=" + str(seed)
        entropy_str = "{self.entropy}"

        self.num_batches = num_batches  # number of batches trained on
        self.batch_size = 10000  # number of steps used to compute each policy update
        self.max_ep_len = 1000  # maximum episode length
        self.learning_rate = 3e-2
        self.gamma = 1.0  # the discount factor
        self.use_baseline = True
        self.normalize_advantage = True
        self.constant_ask_frequency = constant_ask_frequency
        self.collect_initial = collect_initial

        # output config
        self.output_path = "results/{}-{}-{}-{}-{}-{}/".format(
            self.env_name, entropy, self.constant_ask_frequency, self.collect_initial, seed_str, current_time
        )
        self.model_output = self.output_path + "model.weights/"
        self.log_path = self.output_path + "log.txt"
        self.scores_output = self.output_path + "scores.npy"
        self.plot_output = self.output_path + "scores.png"
        self.correlation_output = self.output_path + "correlation.npy"
        self.record_path = self.output_path
        self.record_freq = 5
        self.summary_freq = 1

        # parameters for the policy and baseline models
        self.n_layers = 1
        self.layer_size = 64

        # hyperparameters for PPO
        self.eps_clip = 0.2
        self.update_freq = 20

        # since we start new episodes for each batch
        assert self.max_ep_len <= self.batch_size
        if self.max_ep_len < 0:
            self.max_ep_len = self.batch_size


class config_cheetah:
    def __init__(self, seed, entropy = 0.1, constant_ask_frequency = 1000, collect_initial = 0):
        self.env_name = "HalfCheetahBulletEnv-v0"
        self.record = True
        self.entropy = entropy
        seed_str = "seed=" + str(seed)
        entropy_str = "{self.entropy}"


        # model and training config
        self.num_batches = 2
        # self.num_batches = 100  # number of batches trained on
        self.batch_size = 10000  # number of steps used to compute each policy update
        self.max_ep_len = 1000  # maximum episode length
        self.learning_rate = 3e-2
        self.gamma = 0.9  # the discount factor
        self.use_baseline = True
        self.normalize_advantage = True
        self.constant_ask_frequency = constant_ask_frequency
        self.collect_initial = collect_initial
        
        # output config
        self.output_path = "results/{}-{}-{}-{}-{}/".format(
            self.env_name, entropy, self.constant_ask_frequency, self.collect_initial, seed_str
        )
        self.model_output = self.output_path + "model.weights/"
        self.log_path = self.output_path + "log.txt"
        self.scores_output = self.output_path + "scores.npy"
        self.plot_output = self.output_path + "scores.png"
        self.record_path = self.output_path
        self.record_freq = 5
        self.summary_freq = 1


        # parameters for the policy and baseline models
        self.n_layers = 2
        self.layer_size = 64

        # hyperparameters for PPO
        self.eps_clip = 0.1
        self.update_freq = 10

        # since we start new episodes for each batch
        assert self.max_ep_len <= self.batch_size
        if self.max_ep_len < 0:
            self.max_ep_len = self.batch_size


def get_config(env_name, seed=12, entropy=0.1, constant_ask_frequency=1000, collect_initial=0, num_batches=100):
    if env_name == "cartpole":
        return config_cartpole(seed, entropy, constant_ask_frequency, collect_initial)
    elif env_name == "pendulum":
        print("entropy: ", entropy)
        return config_pendulum(seed, entropy, constant_ask_frequency, collect_initial, num_batches)
    elif env_name == "cheetah":
        return config_cheetah(seed, entropy, constant_ask_frequency, collect_initial)
