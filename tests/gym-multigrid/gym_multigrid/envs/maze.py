from typing import Final, Literal, TypedDict, TypeAlias

from gymnasium import spaces
import numpy as np
from numpy.typing import NDArray

from gym_multigrid.core.agent import Agent, AgentT, MazeActions
from gym_multigrid.core.grid import Grid
from gym_multigrid.core.object import Floor, Flag, Obstacle, WorldObjT
from gym_multigrid.core.world import MazeWorld, World
from gym_multigrid.multigrid import MultiGridEnv
from gym_multigrid.typing import Position
from gym_multigrid.utils.map import distance_area_point, load_text_map


class ObservationDict(TypedDict):
    agent: NDArray
    background: NDArray
    flag: NDArray
    obstacle: NDArray


Observation: TypeAlias = ObservationDict | NDArray


class MazeSingleAgentEnv(MultiGridEnv):
    """
    Environment with a single agent and multiple flags
    """

    def __init__(
        self,
        map_path: str,
        max_steps: int = 100,
        flag_reward: float = 1.0,
        obstacle_penalty_ratio: float = 0.0,
        step_penalty_ratio: float = 0.01,
        observation_option: Literal["positional", "map"] = "map",
        render_mode: Literal["human", "rgb_array"] = "rgb_array",
    ):
        """
        Initialize a new single agent maze environment

        Parameters
        ----------
        map_path : str
            Path to the map file.
        max_steps : int = 100
            Maximum number of steps that the agent can take.
        flag_reward : float = 1.0
            Reward given to the agent for reaching a flag.
        obstacle_penalty_ratio : float = 0.0
            Penalty given to the agent for hitting an obstacle.
        step_penalty_ratio : float = 0.01
            Penalty given to the agent for each step taken.
        observation_option : Literal["positional", "map"] = "map"
            Observation option. If "positional", the observation is the flattened positions of the objects. If "map", the observation is the same with the map.
        render_mode : Literal["human", "rgb_array"] = "rgb_array"
            Render mode.
        """
        agent_view_size: Final[int] = 100

        self.world: Final[World] = MazeWorld
        self.actions_set = MazeActions

        self._map_path: Final[str] = map_path
        self._field_map: Final[NDArray] = load_text_map(map_path)

        height: int
        width: int
        height, width = self._field_map.shape

        self.background: Final[list[Position]] = list(
            zip(*np.where(self._field_map == self.world.OBJECT_TO_IDX["background"]))
        )
        self.obstacle: Final[list[Position]] = list(
            zip(*np.where(self._field_map == self.world.OBJECT_TO_IDX["obstacle"]))
        )
        self.flag: Final[list[Position]] = list(
            zip(*np.where(self._field_map == self.world.OBJECT_TO_IDX["flag"]))
        )

        self.observation_option: Final[Literal["positional", "map"]] = (
            observation_option
        )

        self._flag_reward: Final[float] = flag_reward
        self._obstacle_penalty_ratio: Final[float] = obstacle_penalty_ratio
        self._step_penalty_ratio: Final[float] = step_penalty_ratio

        blue_agent = Agent(
            self.world,
            index=0,
            color="blue",
            bg_color="white",
            view_size=agent_view_size,
            actions=self.actions_set,
            type="agent",
        )

        agents: list[AgentT] = [blue_agent]

        super().__init__(
            width=width,
            height=height,
            max_steps=max_steps,
            see_through_walls=True,
            agents=agents,
            partial_obs=False,
            agent_view_size=agent_view_size,
            actions_set=self.actions_set,
            world=self.world,
            render_mode=render_mode,
        )

    def _set_observation_space(self) -> spaces.Dict | spaces.Box:
        match self.observation_option:
            case "positional":
                observation_space = spaces.Dict(
                    {
                        "agent": spaces.Box(
                            low=np.array([-1, -1]),
                            high=np.array(self._field_map.shape) - 1,
                            dtype=np.int64,
                        ),
                        "background": spaces.Box(
                            low=np.array(
                                [[0, 0] for _ in range(len(self.background))]
                            ).flatten(),
                            high=np.array(
                                [
                                    self._field_map.shape
                                    for _ in range(len(self.background))
                                ]
                            ).flatten()
                            - 1,
                            dtype=np.int64,
                        ),
                        "flag": spaces.Box(
                            low=np.array(
                                [[0, 0] for _ in range(len(self.flag))]
                            ).flatten(),
                            high=np.array(
                                [self._field_map.shape for _ in range(len(self.flag))]
                            ).flatten()
                            - 1,
                            dtype=np.int64,
                        ),
                        "obstacle": spaces.Box(
                            low=np.array(
                                [[0, 0] for _ in range(len(self.obstacle))]
                            ).flatten(),
                            high=np.array(
                                [
                                    self._field_map.shape
                                    for _ in range(len(self.obstacle))
                                ]
                            ).flatten()
                            - 1,
                            dtype=np.int64,
                        ),
                    }
                )

            case "map":
                observation_space = spaces.Box(
                    low=0,
                    high=len(self.world.OBJECT_TO_IDX) - 1,
                    shape=self._field_map.shape,
                    dtype=np.int64,
                )

            case _:
                raise ValueError(
                    f"Invalid observation option: {self.observation_option}"
                )

        return observation_space

    def _gen_grid(self, width, height):
        self.grid = Grid(width, height, self.world)

        for i, j in self.background:
            self.put_obj(Floor(self.world, color="white", type="background"), i, j)

        for i, j in self.obstacle:
            self.put_obj(
                Obstacle(
                    self.world, penalty=self._obstacle_penalty_ratio * self._flag_reward
                ),
                i,
                j,
            )

        for flag_idx, (i, j) in enumerate(self.flag):
            self.put_obj(
                Flag(self.world, index=flag_idx, color="red", bg_color="white"), i, j
            )

        self.init_grid: Grid = self.grid.copy()

        self.place_agent(
            self.agents[0],
            pos=self.background[np.random.randint(0, len(self.background))],
        )

    def reset(self, seed=None) -> tuple[Observation, dict[str, float]]:
        super().reset(seed=seed)

        agent: Agent = self.agents[0]

        assert agent.pos is not None
        self.agent_traj: list[Position] = [agent.pos]
        self.rewards: list[float] = []

        obs: Observation = self._get_obs()
        info: dict[str, float] = self._get_info()

        return obs, info

    def _get_obs(self) -> Observation:
        for a in self.agents:
            assert a.pos is not None

        observation: Observation

        match self.observation_option:
            case "positional":
                observation = {
                    "agent": np.array(self.agents[0].pos),
                    "background": np.array(self.background).flatten(),
                    "flag": np.array(self.flag).flatten(),
                    "obstacle": np.array(self.obstacle).flatten(),
                }
            case "map":
                observation = self._encode_map()

            case _:
                raise ValueError(
                    f"Invalid observation option: {self.observation_option}"
                )

        return observation

    def _encode_map(self) -> NDArray:
        encoded_map: NDArray = np.zeros((self.width, self.height))

        for i, j in self.background:
            encoded_map[i, j] = self.world.OBJECT_TO_IDX["background"]
        for i, j in self.obstacle:
            encoded_map[i, j] = self.world.OBJECT_TO_IDX["obstacle"]
        for i, j in self.flag:
            encoded_map[i, j] = self.world.OBJECT_TO_IDX["flag"]

        assert self.agents[0].pos is not None
        encoded_map[self.agents[0].pos[0], self.agents[0].pos[1]] = (
            self.world.OBJECT_TO_IDX["agent"]
        )

        return encoded_map

    def _get_info(self) -> dict[str, float]:
        assert self.agents[0].pos is not None

        info = {
            "d_a_f": distance_area_point(self.agents[0].pos, self.flag),
            "d_a_ob": distance_area_point(self.agents[0].pos, self.obstacle),
        }
        return info

    def _move_agent(self, action: int, agent: AgentT) -> None:
        next_pos: Position

        assert agent.pos is not None

        match action:
            case self.actions_set.stay:
                next_pos = agent.pos
            case self.actions_set.left:
                next_pos = agent.pos + np.array([0, -1])
            case self.actions_set.down:
                next_pos = agent.pos + np.array([-1, 0])
            case self.actions_set.right:
                next_pos = agent.pos + np.array([0, 1])
            case self.actions_set.up:
                next_pos = agent.pos + np.array([1, 0])
            case _:
                raise ValueError(f"Invalid action: {action}")

        if (
            next_pos[0] < 0
            or next_pos[1] < 0
            or next_pos[0] >= self.height
            or next_pos[1] >= self.width
        ):
            pass  # Do nothing
        else:
            next_cell: WorldObjT | None = self.grid.get(*next_pos)

            bg_color: str = "white"

            if next_cell is None:
                agent.move(next_pos, self.grid, self.init_grid, bg_color=bg_color)
            elif next_cell.can_overlap():
                agent.move(next_pos, self.grid, self.init_grid, bg_color=bg_color)
            else:
                pass

    def _move_agents(self, actions: list[int]) -> None:
        # Move agent
        self._move_agent(actions[0], self.agents[0])

    def _is_agent_on_obj(self, agent_loc: Position | None, obj: list[Position]) -> bool:
        if agent_loc is None:
            assert self.agents[0].pos is not None
            agent_loc = self.agents[0].pos
        else:
            pass

        on_obj: bool = False

        for obj_loc in obj:
            if agent_loc[0] == obj_loc[0] and agent_loc[1] == obj_loc[1]:
                on_obj = True
                break
            else:
                pass

        return on_obj

    def step(
        self, action: int
    ) -> tuple[Observation, float, bool, bool, dict[str, float]]:
        self.step_count += 1

        actions: list[int] = [action]

        self._move_agents(actions)

        assert self.agents[0].pos is not None

        agent_loc: Position = self.agents[0].pos

        terminated: bool = False
        truncated: bool = self.step_count >= self.max_steps

        flag_reward: float = self._flag_reward
        obstacle_penalty: float = flag_reward * self._obstacle_penalty_ratio
        step_penalty: float = flag_reward * self._step_penalty_ratio
        reward: float = 0.0

        if self._is_agent_on_obj(agent_loc, self.flag):
            reward += flag_reward
            terminated = True
        else:
            pass

        if obstacle_penalty != 0:
            if self._is_agent_on_obj(agent_loc, self.obstacle):
                reward -= obstacle_penalty
                terminated = True

            else:
                pass

        else:
            pass

        reward -= step_penalty

        self.agent_traj.append(agent_loc)
        self.rewards.append(reward)

        observation: Observation = self._get_obs()
        info: dict[str, float] = self._get_info()

        return observation, reward, terminated, truncated, info
