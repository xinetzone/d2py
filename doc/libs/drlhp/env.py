import gym
import time
from gym.envs.registration import register
import argparse
from learning_master.drlhp.reward_predictor_core_network import net_cnn
from learning_master.drlhp import HumanPreferencesEnvWrapper
import logging
parser = argparse.ArgumentParser(description=None)
parser.add_argument('-e', '--env', default='soccer', type=str)
from d2py_log import config_logging
args = parser.parse_args()

config_logging('compile.log', "root", maxBytes=5000000, backupCount=7)

def main():

    register(
        id='multigrid-collect-v0',
        entry_point='gym_multigrid.envs:CollectGame4HEnv100x100N2',
    )
    env = gym.make('multigrid-collect-v0')
   
   
  
    wrapper_env = HumanPreferencesEnvWrapper(env,                                               
                                    reward_predictor_network=net_cnn,
                                    segment_length=1,
                                    mp_context='spawn',
                                    n_initial_training_steps=5,
                                    n_initial_prefs=4,
                                    train_reward=True,
                                    collect_prefs=True,
                                    pref_interface_log_level=logging.DEBUG,
                                    reward_predictor_log_level=logging.DEBUG,
                                    env_wrapper_log_level=logging.DEBUG,
                                    prefs_dir=None,
                                    log_dir="testing_logs")
                                             
    
    wrapper_env.reset()
    while True:
        wrapper_env.render(mode='human', highlight=True)
        time.sleep(0.1)
    

        nb_agents = len(wrapper_env.agents)
        ac = [wrapper_env.action_space.sample() for _ in range(nb_agents)]

        obs, reward, done, info = wrapper_env.step(ac)

        if done:
            break
        # from IPython import embed;embed()



if __name__ == "__main__":
    main()