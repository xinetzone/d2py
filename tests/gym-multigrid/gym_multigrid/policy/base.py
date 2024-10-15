import enum
from abc import abstractmethod, ABC
from typing import TypeVar, Type

import numpy as np
from numpy.random import Generator

AgentPolicyT = TypeVar("AgentPolicyT", bound="BaseAgentPolicy")
ObservationT = TypeVar("ObservationT")


class BaseAgentPolicy(ABC):
    """
    Abstract class for CTF enemy policy
    """

    def __init__(
        self,
        action_set: Type[enum.IntEnum] | None = None,
        random_generator: Generator | None = None,
    ) -> None:
        """
        Base class for CTF agent policy.

        Parameters
        ----------
        action_set : enum.IntEnum
            Actions available to the agent.
        random_generator : numpy.random.Generator
            Random number generator. Replace it with the environment's random number generator if needed.
        """
        super().__init__()
        self.name: str = "base"
        self.action_set: Type[enum.IntEnum] = action_set
        self.random_generator: Generator = (
            random_generator
            if random_generator is not None
            else np.random.default_rng()
        )

    @abstractmethod
    def act(self, observation: ObservationT) -> int: ...
