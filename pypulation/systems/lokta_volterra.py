from __future__ import annotations
from typing import List, Union, Any, Callable
from pydantic import validator

from pypulation.core.system import BaseSystem
from pypulation.agents.lokta_volterra import (
    LoktaVolterraPreyAgent,
    LoktaVolterraPredatorAgent,
    CompetitiveLoktaVolterraAgent,
)


class LoktaVolterra(BaseSystem):
    """
    A classical Lokta Volterra System.
    See https://en.wikipedia.org/wiki/Lotka%E2%80%93Volterra_equations for more information.

    This class should not be initialised directly, but should be initialised via the initialise_system method.
    """

    allowed_agents: List[object] = [LoktaVolterraPreyAgent, LoktaVolterraPredatorAgent]
    max_allowed_agents: Dict[str, int] = {"LoktaVolterraPreyAgent": 1, "LoktaVolterraPredatorAgent": 1}

    @classmethod
    def initialise_system_from_agents(agents: List[Any], **kwargs) -> LoktaVolterra:
        """
        Returns an instance of the LoktaVolterra class with agents specified by the agents input.
        """
        return None

    @classmethod
    def initialise_random_system(cls, num_agents: int) -> LoktaVolterra:
        """
        Returns an instance of the LoktaVolterra class with num_random_agents generated agents.
        """
        return None

    @staticmethod
    def random_agents(num_agents: int) -> List[Union[LoktaVolterraPreyAgent, LoktaVolterraPredatorAgent]]:
        """
        Returns a list of randomised Agents (aka Species) of the given num_agents.
        """
        return None
