from pypulation.core.system import BaseSystem
from pypulation.systems.lokta_volterra import LoktaVolterra, CompetitiveLoktaVolterra


# want to be able to spin it up with either a list of agents or a random set.

CLV = CompetitiveLoktaVolterra.initialise_random_system(num_agents=3)

x = CLV.system_ode(CLV.agents[0])

print(CLV.agents[0].population)

for i in range(10):
    CLV.agents[0].population += CLV.system_ode(CLV.agents[0])() * 1
    print(CLV.agents[0].population)

print(CLV.agents)
