from __future__ import annotations
from typing import List, Union, Any
from pydantic import validator

from pypulation.core.system import BaseSystem
from pypulation.agents.lokta_volterra import LoktaVolterraPreyAgent, LoktaVolterraPredatorAgent, CompetitiveLoktaVolterraAgent

class LoktaVolterra(BaseSystem):
    """
    A classical Lokta Volterra System.
    See https://en.wikipedia.org/wiki/Lotka%E2%80%93Volterra_equations for more information.
    
    This class should not be initialised directly, but should be initialised via the initialise_system method.
    """

    allowed_agents: List[object] = [LoktaVolterraPreyAgent, LoktaVolterraPredatorAgent]
    max_allowed_agents: Dict[str, int] = {"LoktaVolterraPreyAgent" : 1, "LoktaVolterraPredatorAgent" : 1}
    min_allowed_agents: Dict[str, int] = {"LoktaVolterraPreyAgent" : 0, "LoktaVolterraPredatorAgent" : 0}


    # could this just get inherited from the base system, and use the allowed agents list?
    @classmethod
    def initialise_system(
        cls,
        input_agents: List[Union[LoktaVolterraPreyAgent, LoktaVolterraPredatorAgent]] = [],
        num_prey: int = None,
        num_predator: int = None,
        **kwargs
    ) -> LoktaVolterra:
        """
        This method returns an instance of the  LoktaVolterra class with agents
        substantiated either from the list of input agents (for analysis of specific cases)
        or random agents (num_random_agents).
        
        When both are defined, this function favours the input_agents.
        """
        
        if input_agents:
            return cls(agents=input_agents)
        elif num_prey in [0,1] and num_predator in [0,1]:
            return cls(agents=cls.random_agents(num_prey=num_prey, num_predator=num_predator))
        else:
            raise ValueError("Pass either a list of input agents or 0 or 1 of each agent type to be randomly generated")


    @staticmethod
    def random_agents(num_prey: int, num_predator: int) -> List[Union[LoktaVolterraPreyAgent, LoktaVolterraPredatorAgent]]:
        """
        Returns a list of two randomised Agents (aka Species) - the prey and the predator.
        """

        agents = []
        agents += [LoktaVolterraPreyAgent.random_agent(alias="prey")] if num_prey else []
        agents += [LoktaVolterraPredatorAgent.random_agent(alias="predator")] if num_predator else []
        
        return agents


class CompetitiveLoktaVolterra(BaseSystem):
    """
    A competitive Lokta Volterra System. No direct predators.
    See https://en.wikipedia.org/wiki/Competitive_Lotka%E2%80%93Volterra_equations for more information
    
    This class should not be initialised directly, but should be initialised via the initialise_system method.
    """

    allowed_agents: List[object] = [CompetitiveLoktaVolterraAgent]


    # could this just get inherited from the base system, and use the allowed agents list?
    @classmethod
    def initialise_system(
        cls,
        input_agents: List[CompetitiveLoktaVolterraAgent] = [],
        num_agents: int = None,
        **kwargs
    ) -> CompetitiveLoktaVolterra:
        """
        This method returns an instance of the  CompetitiveLoktaVolterra class with agents
        substantiated either from the list of input agents (for analysis of specific cases)
        or random agents (num_random_agents).
        
        When both are defined, this function favours the input_agents
        """
        
        if input_agents:
            return cls(agents=input_agents)
        elif num_agents or num_agents == 0:
            return cls(agents=cls.random_agents(num_agents=num_agents))
        else:
            raise ValueError("Pass either a list of input agents or a number of agents to be randomly generated")
        pass


    @staticmethod
    def random_agents(num_agents: int) -> List[CompetitiveLoktaVolterraAgent]:
        """
        Returns a list of randomised Agents (aka Species) of the given num_agents.
        """
        return [
            CompetitiveLoktaVolterraAgent.random_agent(alias=f"species_{i}") for i in range(num_agents)
        ]
