from pydantic import root_validator

from pypulation.core.base.system import BaseSystem
from pypulation.core.discrete.agent import DiscreteAgent


class DiscreteSystem(BaseSystem):
    """
    The base class for generic discrete systems.
    """

    time: int = 0

    def evolve_system(self):
        for agent in self.agents:
            # Problem here is that the populations all change one after the other. Need to do them all at the same time...
            # TODO: fix this (or make this opt out)
            agent.time_evolve()
        self.time += 1

    @root_validator(pre=True)
    def agents_are_discrete(cls, values):
        for v in values["agents"]:
            if not issubclass(type(v), DiscreteAgent):
                raise ValueError(f"Agent must be of Discrete Type. {type(v)} was not")
        return values

