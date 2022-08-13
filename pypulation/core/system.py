from pydantic import BaseModel, validator
from typing import List, Dict, Any
from collections import Counter


class BaseSystem(BaseModel):
    """
    The abstract base class for generic systems.
    """

    time: int = 0

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
                raise ValueError(f"{agent_type} has more than the configured maximum allowed agents ({count} > {max_allowed_agents[agent_type]}).")
        return agents

    @validator("agents")
    def agent_types_min_number(cls, agents, values):
        min_allowed_agents = values.get("min_allowed_agents", {})
        agent_types = [type(x).__name__ for x in agents]
        for agent_type, count in dict(Counter(agent_types)).items():
            if min_allowed_agents.get(agent_type, 0) > count:
                raise ValueError(f"{agent_type} has less than the configured minimum allowed agents ({count} > {min_allowed_agents.get(agent_type, 0)}).")
        return agents

    @property
    def num_agents(self):
        return len(agents)

    def update_time(self, t):
        self.time = t

    def evolve_system(self):
        for x in self.agents:
            # need to be able to pass populations in here...
            x.time_evolve()

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
