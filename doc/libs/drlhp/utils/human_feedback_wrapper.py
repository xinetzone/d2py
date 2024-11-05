import random
import cv2
import gymnasium as gym
import numpy as np

# from model.network_utils import np2torch 
from .preference_db import PreferenceDb

"""
Base class for HumanFeedback and SyntheticFeedback
"""
class Feedback(gym.Wrapper):
    def __init__(self, env, config): # by default uses human feedback
        super().__init__(env)
        self.env = env
        self.config = config
        self.step_id = 0
        self.record = False
        self.pref_db = PreferenceDb.get_instance()

        # buffer to store current pair of trajectory being recorded
        # this is stored seperately from the sampled paths used to train the policy for modularity (so the policy can be changed to other policies)
        self.__reset_traj_buffer()
        self.which_traj = 0 # index to record whether the first or second trajectory is being recorded now
    
        # below subject to change

        self.clip_length = 30 # how long each clip should be
        self.save_pref_db_freq = 100
        self.max_db_size = 1000
        # ask frequency related
        self.ask_frequency_decay = False
        self.constant_ask_frequency = config.constant_ask_frequency
        self.label_schedule = 2e6 # after T frames, rate of labeling should be 2e6 / (T + 2e6)
        self.collect_initial = config.collect_initial # type int. collect some preferences to train the reward function before training agent

        if self.collect_initial:
            self.__collect_initial_preferences()

        print("Collect a preference every {} steps".format(self.constant_ask_frequency))
        print("Clip length = ", self.clip_length)

    def __collect_initial_preferences(self):
        print("collecting initial preferences...")
        while self.pref_db.db_size < self.collect_initial:
            observation, reward, done, info = self.step(self.env.action_space.sample()) # take random action
            if done:
                self.env.reset()
        return

    def __check_ask_schedule(self, step_id):
        """
        TODO: implement actual labeling schedule. Idea: at given timestep, should have a certain number of preferences stored
        """
        if self.ask_frequency_decay:
            rate = (step_id + self.label_schedule) // self.label_schedule # after T frames, rate of labeling should be 2e6 / (T + 2e6)
            if (rate > 1):
                print ("rate > 1: ", rate)
            return step_id % rate == 0
        else: # constant ask frequency
            return step_id % int(self.constant_ask_frequency/2) == 0
    
    def __reset_traj_buffer(self):
        self.traj_buffer = [{
            "observations": [],
            "actions": [],
            "env_rewards": [], # only used for synthetic feedback
            "frames": [], # only used for human feedback
            "num_frames": 0,
        },
        {
            "observations": [],
            "actions": [],
            "env_rewards": [],
            "frames": [],
            "num_frames": 0,
        }] # can't do [{}]*2 because it will create two references to the same dictionary

    def record_additional_data(self, env_reward = None):
        """
        If using human feedback, renders the frame and store it.
        If using synthetic feedback, get the env_reward and store it.
        """
        raise NotImplementedError

    def step(self, action):

        observation, reward, done, info = self.env.step(action)

        if not self.record and self.__check_ask_schedule(self.step_id):
            self.record = True # start recording
        
        if self.record:
            # add step to current trajectory
            i = self.which_traj
            self.traj_buffer[i]["observations"].append(observation.tolist())
            self.traj_buffer[i]["actions"].append(action.tolist())
            self.traj_buffer[i]["num_frames"] += 1
            self.record_additional_data(env_reward = info.get("env_reward", None))

            if self.traj_buffer[i]["num_frames"] == self.clip_length or done:
                self.record = False # stop recording
                if self.which_traj == 1: # if this is already the second traj, i.e. have two full trajs, ask human for preference
                    if self.traj_buffer[0]["num_frames"] == self.clip_length and self.traj_buffer[1]["num_frames"] == self.clip_length: # ask only if the two trajs have the same length
                        self.ask_preference()
                    self.__reset_traj_buffer()
                self.which_traj = 1 - self.which_traj # next time record the other trajectory
        self.step_id += 1

        return observation, reward, done, info
    
    def ask_preference(self):
        raise NotImplementedError
        
    def add_preference(self, obs1, acts1, rs1, obs2, acts2, rs2, preference):
        """
        obs1 etc is a list (length clip_length) of ndarrays (size obs_dim) 
        Add a pair of trajectories and the corresponding preference to the database
        """
        if self.pref_db.db_size > self.max_db_size: # makes sure db size doesn't exceed max
            index = random.randint(0, self.max_db_size)
            self.pref_db.traj1s["observations"][index] = obs1
            self.pref_db.traj2s["observations"][index] = obs1
            self.pref_db.traj1s["actions"][index] = acts1
            self.pref_db.traj2s["actions"][index] = acts2
            self.pref_db.traj1s["env_rewards"][index] = rs1
            self.pref_db.traj2s["env_rewards"][index] = rs2
            self.pref_db.preferences[index] = preference
        else:
            self.pref_db.traj1s["observations"].append(obs1)
            self.pref_db.traj1s["actions"].append(acts1)
            self.pref_db.traj2s["observations"].append(obs2)
            self.pref_db.traj2s["actions"].append(acts2)
            self.pref_db.preferences.append(preference)
            self.pref_db.traj1s["env_rewards"].append(rs1)
            self.pref_db.traj2s["env_rewards"].append(rs2)
            self.pref_db.db_size += 1
        self.pref_db.total_labeled += 1
        # if self.pref_db.db_size % self.save_pref_db_freq == 0:
        #     print (f"{self.pref_db.db_size} preferences collected. Saving database to json...")
        #     self.pref_db.save_to_json(f"{self.config.env_name}_preference_db.json")
        
class HumanFeedback(Feedback):
    def __init__(self, env, config):
        super().__init__(env, config)
        print("--Using human feedback.--")

    def _render_video(self, frames1, frames2):
        for i in range(len(frames1)):
            side_by_side_frame = np.concatenate((frames1[i], frames2[i]), axis=1)
            cv2.imshow("Trajectory 1 on Left, Trajectory 2 on Right", side_by_side_frame)
            cv2.waitKey(1)
        
    def record_additional_data(self, env_reward = None):
        frame = self.env.render(mode='rgb_array')
        self.traj_buffer[self.which_traj]["frames"].append(frame)

    def ask_preference(self):
        """
        TODO: add ability to replay video
        """
        # render two videos
        self._render_video(self.traj_buffer[0]["frames"], self.traj_buffer[1]["frames"])

        # ask human for preference
        print ("Preference (1,2 for preference | Space for equal | Delete/Backspace for incomparable ): ")
        key = cv2.waitKey(0)
        cv2.destroyAllWindows()
        if key == 8 or key == 127: # ASCII code for backspace or delete
            print("Skipping this incomparable pair.")
            return
        if key == ord("1"): 
            preference = 1
            print("1")
        elif key == ord("2"):
            preference = 2
            print("2")
        elif key == 32: # ASCII code for space
            preference = 3
            print("=")
        else:
            print ("Invalid input. Skipping this pair. Use 1 or 2 for preference | Space for equal | Enter/Return for incomparable.")
            return

        # add to database
        self.add_preference(self.traj_buffer[0]["observations"],
                            self.traj_buffer[0]["actions"],
                            self.traj_buffer[0]["env_rewards"],
                            self.traj_buffer[1]["observations"],
                            self.traj_buffer[1]["actions"],
                            self.traj_buffer[1]["env_rewards"],
                            preference)
        return

class SyntheticFeedback(Feedback):
    def __init__(self, env, config):
        super().__init__(env, config)
        print("--Using synthetic feedback.--")

    def record_additional_data(self, env_reward = None):
        assert env_reward is not None, "env_reward should not be None when using synthetic feedback."
        self.traj_buffer[self.which_traj]["env_rewards"].append(env_reward)

    def ask_preference(self):
        # calculate reward for each trajectory
        total_reward1 = np.sum(self.traj_buffer[0]["env_rewards"])
        total_reward2 = np.sum(self.traj_buffer[1]["env_rewards"])
        if total_reward1 > total_reward2:
            preference = 1
        elif total_reward1 < total_reward2:
            preference = 2
        else:
            preference = 3
        self.add_preference(self.traj_buffer[0]["observations"],
                            self.traj_buffer[0]["actions"],
                            self.traj_buffer[0]["env_rewards"],
                            self.traj_buffer[1]["observations"],
                            self.traj_buffer[1]["actions"],
                            self.traj_buffer[1]["env_rewards"],
                            preference)
        return