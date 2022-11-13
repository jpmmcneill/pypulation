from typing import Any, Callable
from scipy.integrate import ode

from pypulation.core.base.system import BaseSystem


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
