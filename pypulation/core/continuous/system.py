from typing import Any, Callable
from scipy.integrate import ode
from pydantic import root_validator

from pypulation.core.base.system import BaseSystem
from pypulation.core.continuous.agent import ContinuousAgent


class ContinuousSystem(BaseSystem):
    """
    The base class for generic continuous systems.
    """

    time: float = 0

    def system_ode(self, agent: Any) -> Callable:
        """
        Returns a function that is the time delta for the given agent.
        This is a required method for any systems - it can access the system (via self) or the agent in question via the agent argument.
        """
        raise NotImplementedError

    def evolve_system(self, timestep: float):
        # maybe give option of non symplectic?
        for agent in self.agents:
            f: callable = self.system_ode(agent)
            r = ode(f).set_integrator('zvode', method='bdf')
            r.set_initial_value(agent.population, self.time)
            t1 = 10
            dt = 1
            print(f"initial: {r.t, r.y}")
            while r.successful() and r.t < t1:
                print(r.t+dt, r.integrate(r.t+dt))
            pass

    @root_validator(pre=True)
    def agents_are_discrete(cls, values):
        for v in values["agents"]:
            if not issubclass(type(v), ContinuousAgent):
                raise ValueError(f"Agent must be of Continuous Type. {type(v)} was not")
        return values
