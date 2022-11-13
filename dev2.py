from pypulation.agents.discrete.logistic_map import LogisticMapAgent
from pypulation.systems.discrete.logistic_map import LogisticMap
from pypulation.core.discrete.agent import DiscreteAgent

x = LogisticMapAgent(
    population = 0.2,
    growth_rate = 3.5
)

lm_sys = LogisticMap.initialise_system_from_agents(agents=[x])

for i in range(100):
    print(x.population)
    x.time_evolve()
