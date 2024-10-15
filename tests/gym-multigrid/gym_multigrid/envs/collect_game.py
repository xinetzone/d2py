import numpy as np
from numpy.typing import NDArray

from gym_multigrid.multigrid import MultiGridEnv
from gym_multigrid.core.world import CollectWorld
from gym_multigrid.core.agent import CollectActions, Agent
from gym_multigrid.core.object import Ball, WorldObjT
from gym_multigrid.core.grid import Grid
from gym_multigrid.typing import Position


class CollectGameEnv(MultiGridEnv):
    """
    Environment in which the agents have to collect the balls
    """

    def __init__(self, *args, actions_set=CollectActions, **kwargs):
        """
        Initialize the CollectGameEnv.

        Parameters
        ----------
        size : int
            Size of grid if square. Default 10
        num_balls : list[int]
            Total number of balls present in environment.
        agents_index : list[int]
            Colour index for each agent.
        balls_index : list[int]
            Colour index for each ball type.
        balls_reward : list[float]
            Reward given for collecting each ball type.
        respawn : bool
            Whether or not balls respawn after being collected.
        """
        self.size = kwargs["size"]
        self.num_balls = kwargs["num_balls"] #np.sum(np.array(kwargs["num_balls"]))
        self.collected_balls = 0
        self.balls_index = kwargs["balls_index"]
        self.balls_reward = kwargs["balls_reward"]
        self.num_ball_types = len(kwargs["balls_index"])
        self.agents_index = kwargs["agents_index"]
        self.respawn = kwargs["respawn"]
        self.world = CollectWorld
        self.actions_set = CollectActions
        partial_obs: bool = False
        self.info = {}
        self.keys = [
            "agent1ball1",
            "agent1ball2",
            "agent1ball3",
            "agent2ball1",
            "agent2ball2",
            "agent2ball3",
        ]

        agents = []
        for i in self.agents_index:
            agents.append(Agent(self.world, i))

        super().__init__(
            grid_size=self.size,
            width=None,
            height=None,
            max_steps=100,
            world=self.world,
            see_through_walls=False,
            agents=agents,
            partial_obs=partial_obs,
            actions_set=self.actions_set,
            render_mode="rgb_array",
        )

    def _gen_grid(self, width: int, height: int):
        """
        Generate grid and place all the balls and agents.

        Parameters
        ----------
        width : int
            width of grid
        height : int
            height of grid
        """
        self.grid = Grid(width, height, self.world)

        # Generate the surrounding walls
        self.grid.horz_wall(0, 0)
        self.grid.horz_wall(0, height - 1)
        self.grid.vert_wall(0, 0)
        self.grid.vert_wall(width - 1, 0)

        if not isinstance(self.num_balls, list):
            raise TypeError(f'Expected num balls to be of type list, \
            however type {type(self.num_balls)} was passed')

        for number, index, reward in zip(
            self.num_balls, self.balls_index, self.balls_reward
        ):
            for _ in range(number):
                self.place_obj(Ball(self.world, index, reward))

        # Randomize the player start position
        for a in self.agents:
            self.place_agent(a)

    def reset(self, *, seed: int | None = None, options: dict | None = None):
        self.collected_balls = 0
        self.info = {
            "agent1ball1": 0,
            "agent1ball2": 0,
            "agent1ball3": 0,
            "agent2ball1": 0,
            "agent2ball2": 0,
            "agent2ball3": 0,
        }
        super().reset(seed=seed)
        state = self.grid.encode()
        return state, self.info

    def _reward(
        self, current_agent: int, rewards: NDArray[np.float_], reward: float = 1
    ) -> None:
        """
        Compute the reward to be given upon success
        """
        rewards[current_agent] += reward
    
    def _respawn(self, color):
        self.place_obj(Ball(self.world, color, self.balls_reward[color]))

    def _handle_pickup(
        self,
        i,
        rewards: NDArray[np.float_],
        fwd_pos: Position,
        fwd_cell: WorldObjT | None,
    ) -> None:
        if fwd_cell and fwd_cell.can_pickup():
            fwd_cell.pos = np.array([-1, -1])
            ball_idx = self.world.COLOR_TO_IDX[fwd_cell.color]
            self.grid.set(*fwd_pos, None)
            if self.respawn:
                self._respawn(ball_idx)
            self.collected_balls += 1
            self._reward(i, rewards, fwd_cell.reward)
            self.info[self.keys[self.num_ball_types * i + ball_idx]] += 1

    def move_agent(
        self,
        rewards: NDArray[np.float_],
        agent_index: int,
        next_cell: WorldObjT | None,
        next_pos: Position,
    ) -> None:
        """
        Method to move given agent to given next position

        Parameters
        ----------
        rewards : NDArray[np.float_]
            array of rewards for each agent
        agent_index : int
            index of agent to move
        next_cell : WorldObjT | None
            object corresponding to next position
        next_pos : Position
            position coordinates to move agent to
        """
        if next_cell is not None:
            if next_cell.type == "ball":
                self._handle_pickup(agent_index, rewards, next_pos, next_cell)
                # move agent to cell
                self.grid.set(*next_pos, self.agents[agent_index])
                self.grid.set(*self.agents[agent_index].pos, None)
                # update agent position variable
                self.agents[agent_index].pos = next_pos
        elif next_cell is None or next_cell.can_overlap():
            self.grid.set(*next_pos, self.agents[agent_index])
            self.grid.set(*self.agents[agent_index].pos, None)
            self.agents[agent_index].pos = next_pos

    def step(
        self, actions: list[int] | NDArray[np.int_]
    ) -> tuple[NDArray[np.int_], NDArray[np.float_], bool, bool, dict]:
        order: list[int] = np.random.permutation(len(actions)).tolist()
        rewards: NDArray[np.float_] = np.zeros(len(actions))
        terminated: bool = False
        truncated: bool = False
        self.step_count += 1
        for i in order:
            if actions[i] == self.actions.north:
                next_pos = self.agents[i].north_pos()
                next_cell = self.grid.get(*next_pos)
                self.move_agent(rewards, i, next_cell, next_pos)
            elif actions[i] == self.actions.east:
                next_pos = self.agents[i].east_pos()
                next_cell = self.grid.get(*next_pos)
                self.move_agent(rewards, i, next_cell, next_pos)
            elif actions[i] == self.actions.south:
                next_pos = self.agents[i].south_pos()
                next_cell = self.grid.get(*next_pos)
                self.move_agent(rewards, i, next_cell, next_pos)
            elif actions[i] == self.actions.west:
                next_pos = self.agents[i].west_pos()
                next_cell = self.grid.get(*next_pos)
                self.move_agent(rewards, i, next_cell, next_pos)
        if not self.respawn and self.collected_balls == self.num_balls:
            terminated = True
        if self.step_count >= self.max_steps:
            truncated = True

        obs = self.grid.encode()
        return obs, rewards, terminated, truncated, self.info

    def phi_dim(self) -> int:
        """
        Helper method to get feature vector dimension

        Returns
        -------
        int
            length of feature vector = number of ball types
        """
        return self.num_ball_types

class CollectGameEvenDist(CollectGameEnv):
    """
        Collect game instance that has the same amount of balls
        for each type of ball present
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.num_balls_per_type = self.num_balls // len(self.balls_index)

    def _gen_grid(self, width: int, height: int) -> None:
        self.grid = Grid(width, height, self.world)

        # Generate the surrounding walls
        self.grid.horz_wall(0, 0)
        self.grid.horz_wall(0, height - 1)
        self.grid.vert_wall(0, 0)
        self.grid.vert_wall(width - 1, 0)

        if not isinstance(self.num_balls, int):
            raise TypeError(f'Expected num balls to be of type int, \
            however type {type(self.num_balls)} was passed')
        assert len(self.balls_reward) == self.num_ball_types
        for ball_type in range(self.num_ball_types):
            for _ in range(self.num_balls_per_type):
                self.place_obj(
                    Ball(
                        self.world,
                        self.balls_index[ball_type],
                        self.balls_reward[ball_type],
                    )
                )
        for a in self.agents:
            self.place_agent(a)

class CollectGameQuadrants(CollectGameEnv):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.num_balls_per_type = self.num_balls // len(self.balls_index)

    def _gen_grid(self, width, height):
        self.grid = Grid(width, height, self.world)

        # Generate the surrounding walls
        self.grid.horz_wall(0, 0)
        self.grid.horz_wall(0, height - 1)
        self.grid.vert_wall(0, 0)
        self.grid.vert_wall(width - 1, 0)

        # place balls
        partitions = [
            (0, 0),
            (width // 2 - 1, height // 2 - 1),
            (width // 2 - 1, 0),
            (0, height // 2),
        ]
        partition_size = (width // 2 - 1, height // 2 - 1)
        for ball_type in range(self.num_ball_types):
            for _ in range(self.num_balls_per_type):
                top = partitions[ball_type]
                self.place_obj(
                    Ball(
                        self.world,
                        self.balls_index[ball_type],
                        self.balls_reward[ball_type],
                    ),
                    top=top,
                    size=partition_size,
                )

        # place agents
        agent_pos = (1, height - 2)
        for a in self.agents:
            self.place_agent(a, agent_pos)
            agent_pos = (agent_pos[0] + 1, agent_pos[1])

class CollectGameRooms(CollectGameEnv):
    def __init__(self, size: int = 11, *args, **kwargs):
        super().__init__(size=size, *args, **kwargs)

    def _gen_grid(self, width: int, height: int):
        self.grid = Grid(width, height, self.world)

        # Generate the surrounding walls
        self.grid.horz_wall(0, 0)
        self.grid.horz_wall(0, height - 1)
        self.grid.vert_wall(0, 0)
        self.grid.vert_wall(width - 1, 0)

        # generate inner walls of rooms
        wall_size = self.width // 2 - 1
        self.grid.horz_wall(0, width // 2, wall_size)
        self.grid.horz_wall(width - wall_size, width // 2, wall_size)
        self.grid.vert_wall(width // 2, 0, wall_size)
        self.grid.vert_wall(width // 2, width - wall_size, wall_size)

        # place agents
        possible_coords = [
            (width // 2, width // 2),
            (width // 2 - 1, width // 2 - 1),
            (width // 2 - 1, width // 2 + 1),
            (width // 2 + 1, width // 2 + 1),
            (width // 2 + 1, width // 2 - 1),
        ]
        for a in self.agents:
            location = self._rand_elem(possible_coords)
            self.place_agent(agent=a, pos=location)

        # place balls
        partitions = [
            (0, 0),
            (width // 2 + 1, width // 2 + 1),
            (width // 2 + 1, 0),
            (0, width // 2 + 1),
        ]
        partition_size = (width // 2 - 1, width // 2 - 1)
        index = 0
        if not isinstance(self.num_balls, int):
            raise TypeError(f'Expected num balls to be of type int, \
            however type {type(self.num_balls)} was passed')
        num_colors: int = len(self.balls_index)
        assert len(self.balls_reward) == num_colors
        num_ball: int = round(self.num_balls / num_colors)
        for ball in range(self.num_balls):
            if ball % num_ball == 0:
                top = partitions[ball // num_ball]
                index = ball // num_ball
                self.place_obj(
                    Ball(self.world, self.balls_index[index], self.balls_reward[index]),
                    top=partitions[3],
                    size=partition_size,
                )
            self.place_obj(
                Ball(self.world, self.balls_index[index], self.balls_reward[index]),
                top=top,
                size=partition_size,
            )

class CollectGameRoomsFixedHorizon(CollectGameRooms):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def step(self, actions):
        obs, rewards, _, truncated, info = super().step(actions)
        return obs, rewards, False, truncated, info

class CollectGameQuadrantsRespawn(CollectGameQuadrants):
    def __init__(self):
        super().__init__()

    def _gen_grid(self, width, height):
        self.grid = Grid(width, height, self.world)

        self.grid.horz_wall(0, 0)
        self.grid.horz_wall(0, height - 1)
        self.grid.vert_wall(0, 0)
        self.grid.vert_wall(width - 1, 0)

        # place balls
        partitions = [(0, 0), (width // 2 - 1, height // 2 - 1), (width // 2 - 1, 0)]
        partition_size = (width // 2 + 1, height // 2 + 1)
        num_ball_per_type = self.num_balls // len(partitions)
        index = 0
        for ball in range(self.num_balls):
            if ball % num_ball_per_type == 0:
                top = partitions[ball // num_ball_per_type]
                index = ball // num_ball_per_type
            self.place_obj(Ball(self.world, index, 1), top=top, size=partition_size)

        # place agents
        agent_pos = (1, height - 2)
        for a in self.agents:
            self.place_agent(a, pos=agent_pos)
            agent_pos = (agent_pos[0] + 1, agent_pos[1])

    def _respawn(self, color):
        partitions = [
            (0, 0),
            (self.width // 2 - 1, self.height // 2 - 1),
            (self.width // 2 - 1, 0),
        ]
        partition_size = (self.width // 2 + 1, self.height // 2 + 1)
        top = partitions[color]
        self.place_obj(Ball(self.world, color, self.balls_reward[color]), top=top, size=partition_size)
