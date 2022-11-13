from __future__ import annotations
from typing import List, Union, Any, Callable
from scipy.stats import beta
from networkx import fast_gnp_random_graph, draw_networkx
import matplotlib.pyplot as plt
import numpy


from pypulation.core.continuous.system import ContinuousSystem
from pypulation.agents.continuous.competitive_lokta_volterra import CompetitiveLoktaVolterraAgent


class CompetitiveLoktaVolterra(ContinuousSystem):
    """
    A competitive Lokta Volterra System. No direct predators.
    See https://en.wikipedia.org/wiki/Competitive_Lotka%E2%80%93Volterra_equations for more information

    This class should not be initialised directly, but should be initialised via either the initialise_system_from_agents or random_agents class methods.
    """

    allowed_agents: List[object] = [CompetitiveLoktaVolterraAgent]
    competition_matrix: Dict[str, Dict[str, float]] = {}

    # TODO: validate that this matrix has keys (and keys underneath) that correspond to the aliases of the species in the system

    def _update_competition_matrix(self, matrix: Dict[str, Dict[str, float]]):
        self.competition_matrix = matrix

    def system_ode(self, agent: CompetitiveLoktaVolterraAgent) -> Callable:
        def interaction_term():
            interactions = self.competition_matrix.get(agent.alias, {})
            result = 0
            for _agent in self.agents:
                # interaction matrix is 1 along the diagonals - elsewhere there is assumed to be no interaction
                interation_strength = 1 if _agent.alias == agent.alias else interactions.get(_agent.alias, 0)
                result += interation_strength * _agent.population
            return result

        def clva_ode():
            return agent.growth_rate * agent.population * (1 - interaction_term() / agent.carrying_capacity)

        return clva_ode

    @classmethod
    def initialise_system_from_agents(agents: List[Any], **kwargs) -> CompetitiveLoktaVolterra:
        """
        Returns an instance of the CompetitiveLoktaVolterra class with agents specified by the agents input.
        """
        return cls(agents=agents)

    @classmethod
    def initialise_random_system(cls, num_agents: int, **kwargs) -> CompetitiveLoktaVolterra:
        """
        Returns an instance of the CompetitiveLoktaVolterra class with num_agents randomly generated agents.
        """
        clazz = cls(agents=cls.random_agents(num_agents=num_agents))
        matrix = clazz.generate_random_competition_matrix(clazz.agents, **kwargs)
        clazz._update_competition_matrix(matrix)
        return clazz

    @staticmethod
    def random_agents(num_agents: int) -> List[CompetitiveLoktaVolterraAgent]:
        """
        Returns a list of randomised Agents (aka Species) of the given num_agents.
        """
        return [CompetitiveLoktaVolterraAgent.random_agent(alias=f"species_{i}") for i in range(num_agents)]

    @staticmethod
    def generate_random_competition_matrix(
        agents: List[CompetitiveLoktaVolterraAgent],
        inter_species_coupling: float = 0.7,
        distribution: Callable = None,
        **kwargs
    ) -> Dict[str, Dict[str, float]]:
        """
        Generates a competition matrix required for random system initialisation.
        This is implemented via a generated Erdős-Rényi graph of the number of specified agents.
        Edges correspond to two agents having a non zero competition matrix.
        Elements of the competition matrix are drawn from a beta distribution by default.
        """
        sys = fast_gnp_random_graph(n=len(agents), p=inter_species_coupling)

        def _get_random_num(**kwargs) -> float:
            if distribution:
                coupling=distribution(**kwargs)
            else:
                coupling=beta.rvs(a=4, b=4)
            return coupling
        
        matrix = {}
        for i, first_agent in enumerate(agents):
            row = {}
            for j, second_agent in enumerate(agents):
                if j in sys.adj.get(i, {}).keys() and i != j:
                    row.update({second_agent.alias: _get_random_num(**kwargs)})
            matrix.update({first_agent.alias: row})
        return matrix
