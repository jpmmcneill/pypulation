from numpy import append

from pydantic import BaseModel, validator

from pypulation.config.config import logging

class BaseAgent(BaseModel):
    """
    The abstract base class for system generic agents.
    """

    alias: str
    population: float = 1

    def _time_evolve(self):
        if logging.logging_enabled:
            self._log_results()
        self.time_evolve()
            
    def time_evolve(self):
        raise NotImplementedError

    def _log_results(self):
        logging.logger_append("agent_alias", self.alias)
        logging.logger_append("population", self.population)

    @classmethod
    def random_agent(cls):
        raise NotImplementedError
