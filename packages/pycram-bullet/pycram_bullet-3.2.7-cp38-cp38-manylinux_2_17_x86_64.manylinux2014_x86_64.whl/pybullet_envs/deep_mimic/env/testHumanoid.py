from pycram_bullet_utils import bullet_client
import time
import math
import motion_capture_data
from pycram_bullet_envs.deep_mimic.env import humanoid_stable_pd
import pycram_bullet_data
import pycram_bullet as p1
import humanoid_pose_interpolator
import numpy as np

pycram_bullet_client = bullet_client.BulletClient(connection_mode=p1.GUI)

pycram_bullet_client.setAdditionalSearchPath(pycram_bullet_data.getDataPath())
z2y = pycram_bullet_client.getQuaternionFromEuler([-math.pi * 0.5, 0, 0])
#planeId = pycram_bullet_client.loadURDF("plane.urdf",[0,0,0],z2y)
planeId = pycram_bullet_client.loadURDF("plane_implicit.urdf", [0, 0, 0],
                                   z2y,
                                   useMaximalCoordinates=True)
pycram_bullet_client.changeDynamics(planeId, linkIndex=-1, lateralFriction=0.9)
#print("planeId=",planeId)

pycram_bullet_client.configureDebugVisualizer(pycram_bullet_client.COV_ENABLE_Y_AXIS_UP, 1)
pycram_bullet_client.setGravity(0, -9.8, 0)

pycram_bullet_client.setPhysicsEngineParameter(numSolverIterations=10)

mocapData = motion_capture_data.MotionCaptureData()
#motionPath = pycram_bullet_data.getDataPath()+"/data/motions/humanoid3d_walk.txt"
motionPath = pycram_bullet_data.getDataPath() + "/data/motions/humanoid3d_backflip.txt"
mocapData.Load(motionPath)
timeStep = 1. / 600
useFixedBase = False
humanoid = humanoid_stable_pd.HumanoidStablePD(pycram_bullet_client, mocapData, timeStep, useFixedBase)
isInitialized = True

pycram_bullet_client.setTimeStep(timeStep)
pycram_bullet_client.setPhysicsEngineParameter(numSubSteps=2)
timeId = pycram_bullet_client.addUserDebugParameter("time", 0, 10, 0)


def isKeyTriggered(keys, key):
  o = ord(key)
  if o in keys:
    return keys[ord(key)] & pycram_bullet_client.KEY_WAS_TRIGGERED
  return False


animating = False
singleStep = False
humanoid.resetPose()
t = 0
while (1):

  keys = pycram_bullet_client.getKeyboardEvents()
  #print(keys)
  if isKeyTriggered(keys, ' '):
    animating = not animating

  if isKeyTriggered(keys, 'b'):
    singleStep = True

  if animating or singleStep:

    singleStep = False
    #t = pycram_bullet_client.readUserDebugParameter(timeId)
    #print("t=",t)
    for i in range(1):

      #print("t=", t)
      humanoid.setSimTime(t)

      humanoid.computePose(humanoid._frameFraction)
      pose = humanoid._poseInterpolator
      #humanoid.initializePose(pose=pose, phys_model = humanoid._sim_model, initBase=True, initializeVelocity=True)
      #humanoid.resetPose()

      desiredPose = humanoid.computePose(humanoid._frameFraction)
      
      #desiredPose = desiredPose.GetPose()
      #curPose = HumanoidPoseInterpolator()
      #curPose.reset()
      
      s = humanoid.getState()
      #np.savetxt("pb_record_state_s.csv", s, delimiter=",")
      maxForces = [
          0, 0, 0, 0, 0, 0, 0, 200, 200, 200, 200, 50, 50, 50, 50, 200, 200, 200, 200, 150, 90, 90,
          90, 90, 100, 100, 100, 100, 60, 200, 200, 200, 200, 150, 90, 90, 90, 90, 100, 100, 100,
          100, 60
      ]
      
      usePythonStablePD = False
      if usePythonStablePD:
        taus = humanoid.computePDForces(desiredPose, desiredVelocities=None, maxForces=maxForces)
        #Print("taus=",taus)
        humanoid.applyPDForces(taus)
      else:
        humanoid.computeAndApplyPDForces(desiredPose,maxForces=maxForces)

      pycram_bullet_client.stepSimulation()
      t += 1. / 600.

  time.sleep(1. / 600.)
