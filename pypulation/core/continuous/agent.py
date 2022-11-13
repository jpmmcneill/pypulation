from pydantic import BaseModel, validator


class BaseAgent(BaseModel):
    """
    The abstract base class for system generic agents.
    """

    alias: str
    population: float = 1

    def time_evolve(self):
        raise NotImplementedError

    @classmethod
    def random_agent(cls):
        raise NotImplementedError
