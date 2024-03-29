from pydantic import BaseModel, validator

from pypulation.core.base.agent import BaseAgent


class ContinuousAgent(BaseAgent):
    """
    The base class for continuous system generic agents.
    """
