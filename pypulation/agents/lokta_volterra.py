from __future__ import annotations
from pydantic import BaseModel

from pypulation.core.agent import BaseAgent


class LoktaVolterraPreyAgent(BaseAgent):

    self_interaction: float = 1
    pred_interaction: float = 1

    def population_rate(self, populations):
        rate = self.population * (self.self_interaction + self.pred_interaction * populations["pred"])
        return rate

    def time_evolve(self):
        # here we need to integrate the population_rate ODE
        # see https://scicomp.stackexchange.com/questions/29149/what-does-symplectic-mean-in-reference-to-numerical-integrators-and-does-scip
        self.population = 0.5

    @classmethod
    def random_agent(cls, **kwargs) -> LoktaVolterraPreyAgent:
        return cls(**kwargs)


class LoktaVolterraPredatorAgent(BaseAgent):
    def time_evolve(self):
        self.population = 0.5

    @classmethod
    def random_agent(cls, **kwargs) -> LoktaVolterraPredatorAgent:
        return cls(**kwargs)


class CompetitiveLoktaVolterraAgent(BaseAgent):

    growth_rate: float = 0.5
    population: float = 1
    carrying_capacity: float = 10

    def time_evolve(self):
        pass

    @classmethod
    def random_agent(cls, system_size: int = 1, **kwargs) -> CompetitiveLoktaVolterraAgent:
        return cls(**kwargs)
