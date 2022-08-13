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


class CompetitiveLoktaVolterra(BaseSystem):
    """
    A competitive Lokta Volterra System. No direct predators.
    See https://en.wikipedia.org/wiki/Competitive_Lotka%E2%80%93Volterra_equations for more information

    This class should not be initialised directly, but should be initialised via either the initialise_system_from_agents or random_agents class methods.
    """

    allowed_agents: List[object] = [CompetitiveLoktaVolterraAgent]
    competition_matrix: Dict[str, Dict[str, Any]] = {}

    # TODO: validate that this matrix has keys (and keys underneath) that correspond to the aliases of the species in the system

    def system_ode(self, agent: CompetitiveLoktaVolterraAgent) -> Callable:
        def interaction_term(**kwargs):
            interactions = self.competition_matrix.get(agent.alias, {})
            result = 0
            for _agent in self.agents:
                # interaction matrix is 1 along the diagonals - elsewhere there is assumed to be no interaction
                interation_strength = 1 if _agent.alias == agent.alias else interactions.get(_agent.alias, 0)
                result += interation_strength * _agent.population
            return result

        def clva_ode(**kwargs):
            return agent.growth_rate * agent.population * (1 - interaction_term() / agent.carrying_capacity)

        return clva_ode

    @classmethod
    def initialise_system_from_agents(agents: List[Any], **kwargs) -> CompetitiveLoktaVolterra:
        """
        Returns an instance of the CompetitiveLoktaVolterra class with agents specified by the agents input.
        """
        return cls(agents=agents)

    @classmethod
    def initialise_random_system(cls, num_agents: int) -> CompetitiveLoktaVolterra:
        """
        Returns an instance of the CompetitiveLoktaVolterra class with num_agents randomly generated agents.
        """
        return cls(agents=cls.random_agents(num_agents=num_agents))

    @staticmethod
    def random_agents(num_agents: int) -> List[CompetitiveLoktaVolterraAgent]:
        """
        Returns a list of randomised Agents (aka Species) of the given num_agents.
        """
        return [CompetitiveLoktaVolterraAgent.random_agent(alias=f"species_{i}") for i in range(num_agents)]
