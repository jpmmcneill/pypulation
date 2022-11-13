from pypulation.core.base.system import BaseSystem


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

