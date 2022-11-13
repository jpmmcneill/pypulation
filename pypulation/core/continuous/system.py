from pydantic import BaseModel, validator
from typing import List, Dict, Any, Callable
from collections import Counter
from scipy.integrate import ode


class BaseSystem(BaseModel):
    """
    The abstract base class for generic systems.
    """

    time: float = 0

    # for validation
    allowed_agents: List[object]
    max_allowed_agents: Dict[str, int] = {}
    min_allowed_agents: Dict[str, int] = {}

    agents: List[Any]

    @validator("agents")
    def agents_are_of_allowed_type(cls, agents, values):
        allowed_agents = values["allowed_agents"]
        for agent in agents:
            if type(agent) not in allowed_agents:
                raise ValueError(f"Agents must be one of those defined in allowed_agents - namely: {allowed_agents}.")
        return agents

    @validator("agents")
    def agent_types_max_number(cls, agents, values):
        max_allowed_agents = values.get("max_allowed_agents", {})
        agent_types = [type(x).__name__ for x in agents]
        for agent_type, count in dict(Counter(agent_types)).items():
            if max_allowed_agents.get(agent_type) and max_allowed_agents.get(agent_type) < count:
                raise ValueError(
                    f"{agent_type} has more than the configured maximum allowed agents ({count} > {max_allowed_agents[agent_type]})."
                )
        return agents

    @validator("agents")
    def agent_types_min_number(cls, agents, values):
        min_allowed_agents = values.get("min_allowed_agents", {})
        agent_types = [type(x).__name__ for x in agents]
        for agent_type, count in dict(Counter(agent_types)).items():
            if min_allowed_agents.get(agent_type, 0) > count:
                raise ValueError(
                    f"{agent_type} has less than the configured minimum allowed agents ({count} > {min_allowed_agents.get(agent_type, 0)})."
                )
        return agents

    @property
    def num_agents(self):
        return len(agents)

    def update_time(self, t: float):
        self.time = t

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

    @classmethod
    def initialise_system_from_agents(agents: List[Any], **kwargs):
        raise NotImplementedError

    @classmethod
    def initialise_random_system(cls, **kwargs):
        """
        Returns a list of randomised Agents (aka Species) of the given num_agents.
        """
        raise NotImplementedError

    @staticmethod
    def random_agents(**kwargs) -> List[Any]:
        """
        Returns a list of randomised Agents (aka Species) of the given num_agents.
        """
        raise NotImplementedError
