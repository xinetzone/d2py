from typing import Literal, TypeVar

import numpy as np
from numpy.random import Generator
from numpy.typing import NDArray

from gym_multigrid.core.agent import ActionsT, CtfActions
from gym_multigrid.core.world import WorldT, CtfWorld
from gym_multigrid.policy.base import BaseAgentPolicy, ObservationT
from gym_multigrid.policy.ctf.utils import a_star
from gym_multigrid.utils.map import position_in_positions, closest_area_pos
from gym_multigrid.typing import Position

ObservationDictT = TypeVar("ObservationDictT", bound=dict)
CtfPolicyT = TypeVar("CtfPolicyT", bound="CtfPolicy")


class CtfPolicy(BaseAgentPolicy):
    """
    Abstract class for Capture the Flag agent policy
    """

    def act(self, observation: ObservationDictT, curr_pos: Position) -> int:
        """
        Determine the action to take.

        Parameters
        ----------
        observation : ObservationDictT
            Observation dictionary (dict from the env).

        Returns
        -------
        int
            Action to take.
        """
        raise NotImplementedError


class RwPolicy(CtfPolicy):
    """
    Random walk policy

    Attributes:
        name: str
            Policy name
        random_generator: numpy.random.Generator
            Random number generator. Replace it with the environment's random number generator if needed.
    """

    def __init__(
        self,
        action_set: ActionsT = CtfActions,
        random_generator: Generator | None = None,
    ) -> None:
        """
        Initialize the RW policy.

        Parameters
        ----------
        action_set : gym_multigrid.core.agent.ActionsT | None
            Actions available to the agent.
        random_generator : numpy.random.Generator
            Random number generator. Replace it with the environment's random number generator if needed.
        """
        super().__init__(action_set, random_generator)
        self.name = "rw"

    def act(
        self, observation: ObservationT | None = None, curr_pos: Position | None = None
    ) -> int:
        return self.random_generator.integers(0, len(self.action_set))


class DestinationPolicy(CtfPolicy):
    """
    Policy that always tries to reach a destination with possible randomness in action selection.

    Attributes:
        name: str
            Policy name
    """

    def __init__(
        self,
        field_map: NDArray | None = None,
        action_set: ActionsT = CtfActions,
        random_generator: Generator | None = None,
        randomness: float = 0.75,
    ) -> None:
        """
        Initialize the policy.

        Parameters
        ----------
        field_map : numpy.typing.NDArray
            Field map of the environment.
        actions : gym_multigrid.core.agent.ActionsT
            Actions available to the agent.
        randomness : float
            Probability of taking an optimal action.
        """
        super().__init__(action_set, random_generator)
        self.name = "destination"
        self.field_map: NDArray | None = field_map
        self.randomness: float = randomness

    def get_target(self, observation: ObservationDictT, curr_pos: Position) -> Position:
        """
        Get the target position of the agent.

        Parameters
        ----------
        observation : ObservationDictT
            Observation dictionary (dict from the env).

        Returns
        -------
        Position
            Target position of the agent.
        """
        # Implement this method
        ...

    def act(self, observation: ObservationDictT, curr_pos: Position) -> int:
        """
        Determine the action to take.

        Parameters
        ----------
        observation : ObservationDictT
            Observation dictionary (dict from the env).

        Returns
        -------
        int
            Action to take.
        """

        start_np: NDArray = np.array(curr_pos)
        target_np: NDArray = np.array(self.get_target(observation, curr_pos))
        # Convert start and target to tuple from NDArray
        start: Position = tuple(start_np)
        target: Position = tuple(target_np)
        shortest_path = a_star(start, target, self.field_map)
        optimal_loc: Position = np.array(
            shortest_path[1] if len(shortest_path) > 1 else target
        )

        # Determine if the agent should take the optimal action
        is_action_optimal: bool = self.random_generator.choice(
            [True, False], p=[self.randomness, 1 - self.randomness]
        )

        # If the optimal action is not taken, return a random action
        action: int
        if is_action_optimal:
            action_dir: NDArray = np.array(optimal_loc) - start_np

            # Convert the direction to an action
            # stay: (0,0), left: (0,-1), down: (-1,0), right: (0,1), up: (1,0)
            if np.array_equal(action_dir, np.array([0, 0])):
                action = self.action_set.stay
            elif np.array_equal(action_dir, np.array([0, -1])):
                action = self.action_set.left
            elif np.array_equal(action_dir, np.array([-1, 0])):
                action = self.action_set.down
            elif np.array_equal(action_dir, np.array([0, 1])):
                action = self.action_set.right
            elif np.array_equal(action_dir, np.array([1, 0])):
                action = self.action_set.up
            else:
                raise ValueError("Invalid direction")
        else:
            action = self.random_generator.integers(0, len(self.action_set))

        return action


class FightPolicy(DestinationPolicy):
    """
    Policy that always tries to fight by taking the shortest path to the opponent agent with some stochasticity.

    Attributes:
        name: str
            Policy name
    """

    def __init__(
        self,
        field_map: NDArray | None = None,
        action_set: ActionsT = CtfActions,
        random_generator: Generator | None = None,
        randomness: float = 0.75,
        ego_agent: Literal["red", "blue"] = "red",
    ) -> None:
        """
        Initialize the policy.

        Parameters
        ----------
        field_map : numpy.typing.NDArray | None = None
            Field map of the environment.
        actions : gym_multigrid.core.agent.ActionsT = CtfActions
            Actions available to the agent.
        randomness : float = 0.75
            Probability of taking an optimal action.
        ego_agent : Literal["red", "blue"] = "red"
            Controlled agent.
        """

        super().__init__(field_map, action_set, random_generator, randomness)
        self.name = "fight"
        self.ego_agent: Literal["red", "blue"] = ego_agent

    def get_target(self, observation: ObservationDictT, curr_pos: Position) -> Position:
        opponent_agent: Literal["red_agent", "blue_agent"] = (
            "blue_agent" if self.ego_agent == "red" else "red_agent"
        )

        opponent_pos_np: NDArray = observation[opponent_agent].reshape(-1, 2)
        opponent_pos: list[Position] = [tuple(pos) for pos in opponent_pos_np]

        target: Position = closest_area_pos(curr_pos, opponent_pos)

        return target


class CapturePolicy(DestinationPolicy):
    """
    Policy that always tries to capture the flag by taking the shortest path to the opponent flag with some stochasticity.

    Attributes:
        name: str
            Policy name
    """

    def __init__(
        self,
        field_map: NDArray | None = None,
        action_set: ActionsT = CtfActions,
        random_generator: Generator | None = None,
        randomness: float = 0.75,
        ego_agent: Literal["red", "blue"] = "red",
    ) -> None:
        """
        Initialize the policy.

        Parameters
        ----------
        field_map : numpy.typing.NDArray | None = None
            Field map of the environment.
        actions : gym_multigrid.core.agent.ActionsT = CtfActions
            Actions available to the agent.
        randomness : float = 0.75
            Probability of taking an optimal action.
        ego_agent : Literal["red", "blue"] = "red"
            Controlled agent.
        """

        super().__init__(field_map, action_set, random_generator, randomness)
        self.name = "capture"
        self.ego_agent: Literal["red", "blue"] = ego_agent

    def get_target(self, observation: ObservationDictT, curr_pos: Position) -> Position:
        match self.ego_agent:
            case "red":
                assert "blue_flag" in observation
                return observation["blue_flag"]
            case "blue":
                assert "red_flag" in observation
                return observation["red_flag"]


class PatrolPolicy(DestinationPolicy):
    """
    Policy that always tries to patrol around the border between blue and red territories with some stochasticity.

    Attributes:
        name: str
            Policy name
    """

    def __init__(
        self,
        field_map: NDArray | None = None,
        action_set: ActionsT = CtfActions,
        random_generator: Generator | None = None,
        randomness: float = 0.75,
        ego_agent: Literal["red", "blue"] = "red",
        world: WorldT = CtfWorld,
    ) -> None:
        """
        Initialize the policy.

        Parameters
        ----------
        field_map : numpy.typing.NDArray | None = None
            Field map of the environment.
        actions : gym_multigrid.core.agent.ActionsT = CtfActions
            Actions available to the agent.
        randomness : float = 0.75
            Probability of taking an optimal action.
        ego_agent : Literal["red", "blue"] = "red"
            Controlled agent.
        world : gym_multigrid.core.world.WorldT = CtfWorld
            World object where the policy is applied.
        """

        super().__init__(field_map, action_set, random_generator, randomness)
        self.name = "patrol"
        self.ego_agent: Literal["red", "blue"] = ego_agent
        self.world: WorldT = world

        self.directions: list[Position] = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        self.border: list[Position]
        self.obstacle: list[Position]
        self.border, self.obstacle = self.locate_border(world, self.directions)

    def get_target(self, observation: ObservationDictT, curr_pos: Position) -> Position:

        if position_in_positions(curr_pos, self.border):
            possible_next_pos: list[Position] = [
                (pos[0] + dir[0], pos[1] + dir[1])
                for pos in self.border
                for dir in self.directions
            ]
            optimal_locs: list[Position] = [
                pos
                for pos in possible_next_pos
                if position_in_positions(pos, self.border)
            ]
            target: Position = self.random_generator.choice(optimal_locs)
        else:
            target: Position = closest_area_pos(curr_pos, self.border)

        return target

    def locate_border(
        self, world: WorldT, directions: list[Position]
    ) -> tuple[list[Position], list[Position]]:
        """
        Locate the border between red and blue territories.

        Parameters
        ----------
        ego_agent : Literal["red", "blue"]
            Controlled agent.

        Returns
        -------
        border: list[Position]
            List of positions on the border.
        """

        assert self.world is not None

        own_territory_type: str = (
            "red_territory" if self.ego_agent == "red" else "blue_territory"
        )
        opponent_territory_type: str = (
            "red_territory" if self.ego_agent == "blue" else "blue_territory"
        )

        own_territory: list[Position] = list(
            zip(*np.where(self.field_map == world.OBJECT_TO_IDX[own_territory_type]))
        )
        opponent_territory: list[Position] = list(
            zip(
                *np.where(
                    self.field_map == world.OBJECT_TO_IDX[opponent_territory_type]
                )
            )
        )
        obstacle: list[Position] = list(
            zip(*np.where(self.field_map == world.OBJECT_TO_IDX["obstacle"]))
        )

        border: list[Position] = []

        for loc in own_territory:
            for dir in directions:
                new_loc: Position = (loc[0] + dir[0], loc[1] + dir[1])
                if position_in_positions(new_loc, opponent_territory + obstacle):
                    border.append(new_loc)
                    break
                else:
                    pass

        return border, obstacle


class PatrolFightPolicy(PatrolPolicy):
    """
    Policy that always tries to patrol around the border between blue and red territories and, once the opponent agent enters the ego territory, it tries to fight by taking the shortest path the opponent.

    Attributes:
        name: str
            Policy name
    """

    def __init__(
        self,
        field_map: NDArray | None = None,
        action_set: ActionsT = CtfActions,
        random_generator: Generator | None = None,
        randomness: float = 0.75,
        ego_agent: Literal["red", "blue"] = "red",
        world: WorldT = CtfWorld,
    ) -> None:
        """
        Initialize the policy.

        Parameters
        ----------
        field_map : numpy.typing.NDArray | None = None
            Field map of the environment.
        actions : gym_multigrid.core.agent.ActionsT = CtfActions
            Actions available to the agent.
        randomness : float = 0.75
            Probability of taking an optimal action.
        ego_agent : Literal["red", "blue"] = "red"
            Controlled agent.
        world : gym_multigrid.core.world.WorldT = CtfWorld
            World object where the policy is applied.
        """

        super().__init__(
            field_map, action_set, random_generator, randomness, ego_agent, world
        )
        self.name = "patrol_fight"

    def get_target(self, observation: ObservationDictT, curr_pos: Position) -> Position:
        opponent_agent: Literal["red_agent", "blue_agent"] = (
            "blue_agent" if self.ego_agent == "red" else "red_agent"
        )
        ego_territory: Literal["red_territory", "blue_territory"] = (
            "red_territory" if self.ego_agent == "red" else "blue_territory"
        )

        opponent_pos_np: NDArray = observation[opponent_agent].reshape(-1, 2)
        opponent_pos: list[Position] = [tuple(pos) for pos in opponent_pos_np]

        ego_territory_pos_np: NDArray = observation[ego_territory].reshape(-1, 2)
        ego_territory_pos: list[Position] = [tuple(pos) for pos in ego_territory_pos_np]

        # Check if the opponent agent is in the ego territory
        is_opponent_in_ego_territory: bool = False
        for pos in opponent_pos:
            if position_in_positions(pos, ego_territory_pos):
                is_opponent_in_ego_territory = True
                break
            else:
                pass

        target: Position = (
            closest_area_pos(curr_pos, opponent_pos)
            if is_opponent_in_ego_territory
            else super().get_target(observation, curr_pos)
        )

        return target
