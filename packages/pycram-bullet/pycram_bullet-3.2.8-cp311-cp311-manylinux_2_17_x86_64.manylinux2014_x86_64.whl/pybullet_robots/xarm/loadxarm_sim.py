import pycram_bullet as p
import pycram_bullet_data as pd
import math
import time
import numpy as np
import pycram_bullet_robots.xarm.xarm_sim as xarm_sim

p.connect(p.GUI)
p.setAdditionalSearchPath(pd.getDataPath())

timeStep=1./60.
p.setTimeStep(timeStep)
p.setGravity(0,0,-9.8)
 
xarm = xarm_sim.XArm6Sim(p,[0,0,0])
while (1):
	xarm.step()
	p.stepSimulation()
	time.sleep(timeStep)
	
