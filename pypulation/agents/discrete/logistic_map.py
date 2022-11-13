from __future__ import annotations

from pydantic import validator

from pypulation.core.discrete.agent import DiscreteAgent


class LogisticMapAgent(DiscreteAgent):

    growth_rate: float = 2
    population: float = 0.5
    alias: str = 'logistic_map_population'

    def time_evolve(self):
        self.population = self.growth_rate * self.population * ( 1 - self.population )

    @classmethod
    def random_agent(cls, **kwargs) -> LoktaVolterraPreyAgent:
        return cls(**kwargs)

    @validator('population')
    def ensure_population_between_0_1(cls, v):
        if v > 1 or v < 0:
            raise ValueError("Logistic Map initial population must be between 0 and 1")
        return v
