import pycram_bullet as p
import pycram_bullet_data as pd
import math
import time
import numpy as np
from pycram_bullet_envs.examples import panda_sim

p.connect(p.GUI)
p.configureDebugVisualizer(p.COV_ENABLE_Y_AXIS_UP,1)
p.setAdditionalSearchPath(pd.getDataPath())

timeStep=1./60.
p.setTimeStep(timeStep)
p.setGravity(0,-9.8,0)
 
panda = panda_sim.PandaSim(p,[0,0,0])
while (1):
	panda.step()
	p.stepSimulation()
	time.sleep(timeStep)
	
