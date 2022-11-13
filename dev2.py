from pypulation.agents.discrete.logistic_map import LogisticMapAgent
from pypulation.systems.discrete.logistic_map import LogisticMap
from pypulation.core.discrete.agent import DiscreteAgent

from pypulation.config.config import logging

x = LogisticMapAgent(
    population = 0.2,
    growth_rate = 3.5
)

lm_sys = LogisticMap.initialise_system_from_agents(agents=[x])


for i in range(100):
    # print(x.population)
    lm_sys.evolve_system()

logging.cache_logger()
