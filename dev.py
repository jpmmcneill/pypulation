from pypulation.core.system import BaseSystem
from pypulation.systems.lokta_volterra import LoktaVolterra, CompetitiveLoktaVolterra


# want to be able to spin it up with either a list of agents or a random set.
#

CLV = CompetitiveLoktaVolterra.initialise_system(num_agents=3)

LV = LoktaVolterra.initialise_system(num_predator=1, num_prey=1)

print(LV.agents)
LV.evolve_system()
print(LV.agents)
