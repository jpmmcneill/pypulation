from pydantic import BaseModel, validator

from pypulation.core.base.agent import BaseAgent


class DiscreteAgent(BaseAgent):
    """
    The base class for discrete system generic agents.
    """
