import set_env
import logging
import multiprocessing as mp
import sys
import time
from pathlib import Path
from d2py.utils.log_config import config_logging
root_dir = Path(".").resolve()
sys.path.extend([str(root_dir.parents[2]/"tests/gym-multigrid")])

logger_dir = root_dir/".temp"
logger_dir.mkdir(parents=True, exist_ok=True)
temp_dir = root_dir/"images"
temp_dir.mkdir(parents=True, exist_ok=True)

logger_name = "drlhp"
logger = logging.getLogger(logger_name)
config_logging(f'{logger_dir}/{logger_name}.log', logger_name, maxBytes=50000, backupCount=2)


from pathlib import Path
import imageio
from gym_multigrid.envs.collect_game import CollectGameEnv
from drlhp.env import HumanPreferencesEnvWrapper
from drlhp.model import net_cnn

kwargs={
    "render_mode": "human",
    "size": 100,
    "num_balls": [5,],
    "agents_index": [1, 2, 3],  # green, purple
    "balls_index": [0,],  # red, orange, yellow
    "balls_reward": [1,],
    "respawn": False,
}
origin_env = CollectGameEnv(**kwargs)

if __name__ == "__main__":
    # mp.freeze_support()
    hp_env = HumanPreferencesEnvWrapper(
        origin_env, net_cnn,
        segment_length=100,
        mp_context="spawn",
        n_initial_training_steps=5,
        n_initial_prefs=40,
        train_reward=True,
        collect_prefs=True,
        synthetic_prefs=False,
        pref_interface_log_level=logging.DEBUG,
        reward_predictor_log_level=logging.DEBUG,
        env_wrapper_log_level=logging.DEBUG,
        # prefs_dir=".temp3",
    )
    frames = [hp_env.render()]
    obs, info = hp_env.reset()
    while 1:
        time.sleep(0.1)
        actions = [hp_env.env.action_space.sample() for _ in hp_env.env.agents]
        obs, reward, terminated, truncated, info = hp_env.step(actions)
        frames.append(hp_env.render())
        if terminated or truncated:
            logger.info(f"episode ended after {hp_env.env.step_count} steps")
            logger.info(f"agents collected {hp_env.env.collected_balls} objects")
            break

    from IPython import display
    temp_dir = Path(temp_dir)
    (temp_dir/"animations").mkdir(parents=True, exist_ok=True)
    imageio.mimsave(temp_dir/f"animations/multigrid-collect.gif", frames, duration=0.5)
    display.Image(temp_dir/f"animations/multigrid-collect.gif")
