import math
import random
from typing import Literal, Type, TypeVar, Callable
import numpy as np
import gymnasium as gym
from gymnasium import spaces

from gym_multigrid.core.grid import Grid
from gym_multigrid.core.object import WorldObjT
from gym_multigrid.core.world import DefaultWorld, WorldT
from gym_multigrid.core.agent import ActionsT, AgentT, DefaultActions
from gym_multigrid.typing import Position
from gym_multigrid.utils.rendering import *
from gym_multigrid.utils.window import Window
from gym_multigrid.core.constants import *


MultiGridEnvT = TypeVar("MultiGridEnvT", bound="MultiGridEnv")


class MultiGridEnv(gym.Env):
    """
    2D grid world game environment
    """

    metadata = {"render_modes": ["human", "rgb_array"], "video.frames_per_second": 10}

    def __init__(
        self,
        agents: list[AgentT],
        grid_size: int | None = None,
        width: int | None = None,
        height: int | None = None,
        max_steps: int = 100,
        see_through_walls: bool = False,
        partial_obs: bool = False,
        agent_view_size: int = 7,
        actions_set: Type[ActionsT] = DefaultActions,
        world: WorldT = DefaultWorld,
        render_mode: Literal["human", "rgb_array"] = "rgb_array",
        uncached_object_types: list[str] = [],
    ) -> None:
        self.agents: list[AgentT] = agents
        assert render_mode is None or render_mode in self.metadata["render_modes"]
        self.render_mode = render_mode
        self.uncahed_object_types = uncached_object_types
        # Does the agents have partial or full observation?
        self.partial_obs = partial_obs
        self.agent_view_size = agent_view_size

        # Can't set both grid_size and width/height
        if grid_size:
            assert width == None and height == None
            width = grid_size
            height = grid_size
        else:
            assert width != None and height != None

        self.width: int = width
        self.height: int = height

        # Action enumeration for this environment
        self.actions = actions_set

        # Actions are discrete integer values
        self.action_space = spaces.Discrete(len(self.actions))

        self.world = world

        self.observation_space: spaces.Box | spaces.Dict = self._set_observation_space()

        if self.observation_space is spaces.Box:
            self.ob_dim = np.prod(self.observation_space.shape)
        else:
            pass
        self.ac_dim = self.action_space.n

        # Range of possible rewards
        self.reward_range = (0, 1)

        # Window to use for human rendering mode
        self.window = None

        # Environment configuration
        self.max_steps = max_steps
        self.see_through_walls = see_through_walls

        # Define the empty grid. _gen_grid is supposed to fill this up
        self.grid = Grid(width, height, world)

    def _set_observation_space(self) -> spaces.Box | spaces.Dict:
        if self.partial_obs:
            observation_space = spaces.Box(
                low=0,
                high=255,
                shape=(
                    self.agent_view_size,
                    self.agent_view_size,
                    self.world.encode_dim,
                ),
                dtype="uint8",
            )

        else:
            observation_space = spaces.Box(
                low=0,
                high=255,
                shape=(self.width, self.height, self.world.encode_dim),
                dtype="uint8",
            )

        return observation_space

    def reset(
        self,
        *,
        seed: int | None = None,
        options: dict | None = None,
    ):
        # It is recommended to use the random number generator self.np_random 
        # that is provided by the environment’s base class, gymnasium.Env. 
        # If you only use this RNG, you do not need to worry much about seeding, 
        # but you need to remember to call ``super().reset(seed=seed)`` to make 
        # sure that gymnasium.Env correctly seeds the RNG
        super().reset(seed=seed)
        # Generate a new random grid at the start of each episode
        # To keep the same grid for each episode, call env.seed() with
        # the same seed before calling env.reset()
        self._gen_grid(self.width, self.height)

        # These fields should be defined by _gen_grid
        for a in self.agents:
            assert a.pos is not None
            assert a.dir is not None

        # Item picked up, being carried, initially nothing
        for a in self.agents:
            a.carrying = None

        # Step count since episode start
        self.step_count: int = 0

        # Return first observation
        if self.partial_obs:
            obs = self.gen_obs()
        else:
            obs = [
                self.grid.encode_for_agents(agent_pos=self.agents[i].pos)
                for i in range(len(self.agents))
            ]
        obs = [self.world.normalize_obs * ob for ob in obs]
        info = self._get_info()
        return obs, info
    
    def _get_info(self):
        return {}

    @property
    def steps_remaining(self):
        return self.max_steps - self.step_count

    def __str__(self):
        """
        Produce a pretty string of the environment's grid along with the agent.
        A grid cell is represented by 2-character string, the first one for
        the object and the second one for the color.
        """

        str = ""

        for j in range(self.grid.height):
            for i in range(self.grid.width):
                # if i == self.agent_pos[0] and j == self.agent_pos[1]:
                # str += 2 * AGENT_DIR_TO_STR[self.agent_dir]
                # continue

                c = self.grid.get(i, j)

                if c == None:
                    str += "  "
                    continue

                if c.type == "door":
                    if c.is_open:
                        str += "__"
                    elif c.is_locked:
                        str += "L" + c.color[0].upper()
                    else:
                        str += "D" + c.color[0].upper()
                    continue

                str += OBJECT_TO_STR[c.type] + c.color[0].upper()

            if j < self.grid.height - 1:
                str += "\n"

        return str

    def _gen_grid(self, width, height) -> None:
        self.grid = Grid(width, height, self.world)
        assert False, "_gen_grid needs to be implemented by each environment"

    def _handle_pickup(self, i, rewards, fwd_pos, fwd_cell):
        pass

    def _handle_build(self, i, rewards, fwd_pos, fwd_cell):
        pass

    def _handle_drop(self, i, rewards, fwd_pos, fwd_cell):
        pass

    def _handle_special_moves(self, i, rewards, fwd_pos, fwd_cell):
        pass

    def _handle_switch(self, i, rewards, fwd_pos, fwd_cell):
        pass

    def _reward(self, current_agent, rewards, reward=1):
        """
        Compute the reward to be given upon success
        """
        rewards[current_agent] += reward - 0.9 * (self.step_count / self.max_steps)
        return rewards

    def _rand_int(self, low, high):
        """
        Generate random integer in [low,high[
        """

        return random.randint(low, high)

    def _rand_float(self, low, high):
        """
        Generate random float in [low,high[
        """

        return self.np_random.uniform(low, high)

    def _rand_bool(self):
        """
        Generate random boolean value
        """

        return self.np_random.randint(0, 2) == 0

    def _rand_elem(self, iterable):
        """
        Pick a random element in a list
        """

        lst = list(iterable)
        idx = self._rand_int(0, len(lst) - 1)
        return lst[idx]

    def _rand_subset(self, iterable, num_elems):
        """
        Sample a random subset of distinct elements of a list
        """

        lst = list(iterable)
        assert num_elems <= len(lst)

        out = []

        while len(out) < num_elems:
            elem = self._rand_elem(lst)
            lst.remove(elem)
            out.append(elem)

        return out

    def _rand_pos(self, xLow, xHigh, yLow, yHigh):
        """
        Generate a random (x,y) position tuple
        """

        return (
            self.np_random.randint(xLow, xHigh),
            self.np_random.randint(yLow, yHigh),
        )

    def place_obj(
        self,
        obj: WorldObjT,
        top: Position | None = None,
        size: tuple[int, int] | None = None,
        reject_fn: Callable[["MultiGridEnv", NDArray], bool] | None = None,
        max_tries: float = math.inf,
    ):
        """
        Place an object at an empty position in the grid

        :param top: top-left position of the rectangle where to place
        :param size: size of the rectangle where to place
        :param reject_fn: function to filter out potential positions
        """

        if top is None:
            top = (0, 0)
        else:
            top = (max(top[0], 0), max(top[1], 0))

        if size is None:
            size = (self.grid.width, self.grid.height)

        num_tries = 0

        while True:
            # This is to handle with rare cases where rejection sampling
            # gets stuck in an infinite loop
            if num_tries > max_tries:
                raise RecursionError("rejection sampling failed in place_obj")

            num_tries += 1

            pos = np.array(
                (
                    self._rand_int(top[0], min(top[0] + size[0], self.grid.width - 1)),
                    self._rand_int(top[1], min(top[1] + size[1], self.grid.height - 1)),
                )
            )

            # Don't place the object on top of another object
            if self.grid.get(*pos) != None:
                continue

            # Check if there is a filtering criterion
            if reject_fn and reject_fn(self, pos):
                continue

            break

        self.grid.set(*pos, obj)

        if obj is not None:
            obj.init_pos = pos
            obj.pos = pos

        return pos

    def put_obj(self, obj: WorldObjT, i: int, j: int):
        """
        Put an object at a specific position in the grid
        """

        self.grid.set(i, j, obj)
        obj.init_pos = (i, j)
        obj.pos = (i, j)

    def place_agent(
        self,
        agent: AgentT,
        pos: Position | None = None,
        top: Position | None = None,
        size: tuple[int, int] | None = None,
        rand_dir: bool = False,
        max_tries: float = math.inf,
    ) -> Position:
        """
        Set the agent's starting point at an empty position in the grid
        """
        if pos is not None:
            agent.pos = pos
            self.put_obj(agent, i=pos[0], j=pos[1])
        else:
            agent.pos = None
            pos = self.place_obj(agent, top, size, max_tries=max_tries)
            agent.pos = pos
            agent.init_pos = pos

        if rand_dir:
            agent.dir = self._rand_int(0, 3)
        else:
            agent.dir = 3

        agent.init_dir = agent.dir

        return pos

    def agent_sees(self, a, x, y):
        """
        Check if a non-empty grid position is visible to the agent
        """

        coordinates = a.relative_coords(x, y)
        if coordinates is None:
            return False
        vx, vy = coordinates

        obs = self.gen_obs()
        obs_grid, _ = self.grid.decode(obs["image"])
        obs_cell = obs_grid.get(vx, vy)
        world_cell = self.grid.get(x, y)

        return obs_cell is not None and obs_cell.type == world_cell.type

    def step(
        self, actions: list[int] | NDArray[np.int_]
    ) -> tuple[NDArray[np.int_], NDArray[np.float_], bool, bool, dict]:
        self.step_count += 1

        order = np.random.permutation(len(actions))

        rewards = np.zeros(len(actions))
        terminated = False
        truncated = False

        for i in order:
            if (
                self.agents[i].terminated
                or self.agents[i].paused
                or not self.agents[i].started
                or actions[i] == self.actions.still
            ):
                continue

            # Get the position in front of the agent
            fwd_pos = self.agents[i].front_pos

            # Get the contents of the cell in front of the agent
            fwd_cell = self.grid.get(*fwd_pos)

            # Rotate left
            if actions[i] == self.actions.left:
                self.agents[i].dir -= 1
                if self.agents[i].dir < 0:
                    self.agents[i].dir += 4

            # Rotate right
            elif actions[i] == self.actions.right:
                self.agents[i].dir = (self.agents[i].dir + 1) % 4

            # Move forward
            elif actions[i] == self.actions.forward:
                if fwd_cell is not None:
                    if fwd_cell.type == "goal":
                        terminated = True
                        rewards = self._reward(i, rewards, 1)
                    elif fwd_cell.type == "switch":
                        self._handle_switch(i, rewards, fwd_pos, fwd_cell)
                elif fwd_cell is None or fwd_cell.can_overlap():
                    self.grid.set(*fwd_pos, self.agents[i])
                    self.grid.set(*self.agents[i].pos, None)
                    self.agents[i].pos = fwd_pos
                self._handle_special_moves(i, rewards, fwd_pos, fwd_cell)

            elif "build" in self.actions.available and actions[i] == self.actions.build:
                self._handle_build(i, rewards, fwd_pos, fwd_cell)

            # Pick up an object
            elif actions[i] == self.actions.pickup:
                self._handle_pickup(i, rewards, fwd_pos, fwd_cell)

            # Drop an object
            elif actions[i] == self.actions.drop:
                self._handle_drop(i, rewards, fwd_pos, fwd_cell)

            # Toggle/activate an object
            elif actions[i] == self.actions.toggle:
                if fwd_cell:
                    fwd_cell.toggle(self, fwd_pos)

            # Done action (not used by default)
            elif actions[i] == self.actions.done:
                pass

            else:
                assert False, "unknown action"

        if self.step_count >= self.max_steps:
            truncated = True

        if self.partial_obs:
            obs = self.gen_obs()
        else:
            obs = [
                self.grid.encode_for_agents(agent_pos=self.agents[i].pos)
                for i in range(len(actions))
            ]

        obs = [self.world.normalize_obs * ob for ob in obs]
        info = self._get_info()
        return obs, rewards, terminated, truncated, info

    def gen_obs_grid(self):
        """
        Generate the sub-grid observed by the agents.
        This method also outputs a visibility mask telling us which grid
        cells the agents can actually see.
        """

        grids = []
        vis_masks = []

        for a in self.agents:
            topX, topY, botX, botY = a.get_view_exts()

            grid = self.grid.slice(topX, topY, a.view_size, a.view_size)

            for i in range(a.dir + 1):
                grid = grid.rotate_left()

            # Process occluders and visibility
            # Note that this incurs some performance cost
            if not self.see_through_walls:
                vis_mask = grid.process_vis(
                    agent_pos=(a.view_size // 2, a.view_size - 1)
                )
            else:
                vis_mask = np.ones(shape=(grid.width, grid.height), dtype=np.bool)

            grids.append(grid)
            vis_masks.append(vis_mask)

        return grids, vis_masks

    def gen_obs(self):
        """
        Generate the agent's view (partially observable, low-resolution encoding)
        """

        grids, vis_masks = self.gen_obs_grid()

        # Encode the partially observable view into a numpy array
        obs = [
            grid.encode_for_agents(
                self.world, [grid.width // 2, grid.height - 1], vis_mask
            )
            for grid, vis_mask in zip(grids, vis_masks)
        ]

        return obs

    def get_obs_render(self, obs, tile_size=TILE_PIXELS // 2):
        """
        Render an agent observation for visualization
        """

        grid, vis_mask = self.grid.decode(obs)

        # Render the whole grid
        img = grid.render(self.world, tile_size, highlight_mask=vis_mask)

        return img

    def render(self, close=False, highlight=False, tile_size=TILE_PIXELS):
        """
        Render the whole-grid human view
        """

        if close:
            if self.window:
                self.window.close()
            return

        if self.render_mode == "human" and not self.window:
            self.window = Window("gym_multigrid")
            self.window.show(block=False)

        if highlight:
            # Compute which cells are visible to the agent
            _, vis_masks = self.gen_obs_grid()

            highlight_masks = {
                (i, j): [] for i in range(self.width) for j in range(self.height)
            }

            for i, a in enumerate(self.agents):
                # Compute the world coordinates of the bottom-left corner
                # of the agent's view area
                f_vec = a.dir_vec
                r_vec = a.right_vec
                top_left = (
                    a.pos + f_vec * (a.view_size - 1) - r_vec * (a.view_size // 2)
                )

                # Mask of which cells to highlight

                # For each cell in the visibility mask
                for vis_j in range(0, a.view_size):
                    for vis_i in range(0, a.view_size):
                        # If this cell is not visible, don't highlight it
                        if not vis_masks[i][vis_i, vis_j]:
                            continue

                        # Compute the world coordinates of this cell
                        abs_i, abs_j = top_left - (f_vec * vis_j) + (r_vec * vis_i)

                        if abs_i < 0 or abs_i >= self.width:
                            continue
                        if abs_j < 0 or abs_j >= self.height:
                            continue

                        # Mark this cell to be highlighted
                        highlight_masks[abs_i, abs_j].append(i)

        # Render the whole grid
        img = self.grid.render(
            tile_size,
            highlight_masks=highlight_masks if highlight else None,
            uncached_object_types=self.uncahed_object_types,
        )

        if self.render_mode == "human":
            self.window.show_img(img)

        return img
