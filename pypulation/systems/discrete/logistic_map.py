from __future__ import annotations
from typing import List, Union, Any, Callable
from pydantic import validator

from pypulation.core.discrete.system import DiscreteSystem
from pypulation.agents.discrete.logistic_map import LogisticMapAgent


class LogisticMap(DiscreteSystem):
    """
    The Logistic Map.
    See https://en.wikipedia.org/wiki/Logistic_map for more information.
    """

    allowed_agents: List[object] = [LogisticMapAgent]
    max_allowed_agents: Dict[str, int] = {"LogisticMapAgent": 1}

    @classmethod
    def initialise_system_from_agents(cls, agents: List[Any], **kwargs) -> LogisticMap:
        """
        Returns an instance of the LogisticMap class with agents specified by the agents input.
        """
        return cls(agents=agents)

    @classmethod
    def initialise_random_system(cls) -> LogisticMap:
        """
        Returns an instance of the LogisticMap class with a randomly generated agent.
        """
        return None

    @staticmethod
    def random_agents() -> List[LogisticMapAgent]:
        """
        Returns a list of randomised Agents (aka Species).
        """
        return None
