"""
a simple database for preferences
format: traj1s["observation"][i], traj1s["action"][i], traj2s["observation"][i], traj2s["action"][i], preferences[i] 
    form one pair of trajectories and the corresponding preference

Uses a Singleton pattern to share the database between HumanFeedback wrapper (add pref) and CustomReward wrapper (sample pref)
"""

import json

class PreferenceDb(object):
    _instance = None
    def __init__(self):
        if self._instance is not None:
            raise Exception("Only one instance of PreferenceDatabase is allowed.")
        else:
            # TODO: load from json if json file exists
            
            self.traj1s = {
                "observations": [],
                "actions": [],
                "env_rewards": [],
            }
            self.traj2s = {
                "observations": [],
                "actions": [],
                "env_rewards": [],
            }
            self.preferences = []
            self.db_size = 0 # current size
            self.total_labeled = 0 # total number of preferences collected, including those discarded
            PreferenceDb._instance = self

    @staticmethod
    def get_instance():
        if PreferenceDb._instance is None:
            PreferenceDb()
        return PreferenceDb._instance
    
    @staticmethod
    def save_to_json(filename):
        db = PreferenceDb._instance
        data = {
            "traj1s": db.traj1s,
            "traj2s": db.traj2s,
            "preferences": db.preferences,
            "db_size": db.db_size,
        }
        with open(filename, 'w') as f:
            json.dump(data, f)
