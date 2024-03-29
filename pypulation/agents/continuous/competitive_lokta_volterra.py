from __future__ import annotations

from pypulation.core.continuous.agent import ContinuousAgent


class CompetitiveLoktaVolterraAgent(ContinuousAgent):

    growth_rate: float = 0.5
    population: float = 1
    carrying_capacity: float = 10

    def time_evolve(self):
        pass

    @classmethod
    def random_agent(cls, system_size: int = 1, **kwargs) -> CompetitiveLoktaVolterraAgent:
        return cls(**kwargs)
