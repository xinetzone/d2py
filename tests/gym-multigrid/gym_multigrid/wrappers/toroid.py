import numpy as np
import gymnasium as gym
from gymnasium import ObservationWrapper, spaces


class ToroidObservation(ObservationWrapper):
    """
    Transforms the CollectGame observation grid into agent-centric,
    toroidal observations as described in the appendix of 10.1073/pnas.1907370117
    """

    def __init__(self, env: gym.Env):
        """
        Initialize ToroidObservation Wrapper

        Parameters
        ----------
        env : gymnasium.Env
            gym environment for which the wrapper is being used
        """
        super().__init__(env)
        self.env = env
        self.depth = env.num_ball_types + len(env.agents)
        self.observation_space = spaces.Box(
            shape=(env.width, env.height, self.depth), low=-np.inf, high=np.inf
        )

    def observation(self, obs):
        """
        Modifies default env observation into toroidal-wrapped
        observations for each agent's POV

        Parameters
        ----------
        obs
            default observation used by environment

        Returns
        -------
        obs : List[NDArray]
            list of length num_agents containing transformed observations
        """
        toroids = []
        for a in self.env.agents:
            pos = a.pos
            tor = np.zeros(self.observation_space.shape, dtype="float32")
            for i in range(self.env.width):
                for j in range(self.env.height):
                    new_coords = [i - pos[0], j - pos[1]]
                    obj = self.env.grid.get(i, j)
                    if new_coords[0] < 0:
                        new_coords[0] += self.env.width
                    if new_coords[1] < 0:
                        new_coords[1] += self.env.height
                    if obj is None:
                        continue
                    elif obj.type == "wall":
                        tor[new_coords[1], new_coords[0], self.depth - 1] = 1
                    elif obj.type == "ball":
                        tor[
                            new_coords[1],
                            new_coords[0],
                            self.env.world.COLOR_TO_IDX[obj.color],
                        ] = 1
                    elif obj.type == "agent" and not np.array_equal(obj.pos, pos):
                        tor[new_coords[1], new_coords[0], self.depth - 2] = 1
            toroids.append(tor)
        return toroids
