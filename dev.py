from pypulation.core.system import BaseSystem
from pypulation.systems.competitive_lokta_volterra import CompetitiveLoktaVolterra
from networkx import fast_gnp_random_graph, draw
import matplotlib.pyplot as plt


# want to be able to spin it up with either a list of agents or a random set.

CLV = CompetitiveLoktaVolterra.initialise_random_system(num_agents=5, inter_species_coupling=0.3)

x = CLV.system_ode(CLV.agents[0])

print(CLV.agents[0].population)

for i in range(30):
    CLV.agents[0].population += CLV.system_ode(CLV.agents[0])() * 1
    print(CLV.agents[0].population)

print(CLV.agents)

CLV.evolve_system(timestep = 1)
