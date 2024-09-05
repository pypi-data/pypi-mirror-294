"""Tests for pycram_bullet_envs.minitaur.robots.mini_cheetah.

blaze test -c opt
//robotics/reinforcement_learning/minitaur/robots:mini_cheetah_test
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import math
import numpy as np
from pycram_bullet_envs.minitaur.envs import bullet_client
from pycram_bullet_envs.minitaur.robots import mini_cheetah
from google3.testing.pybase import googletest

PI = math.pi
NUM_STEPS = 500
TIME_STEP = 0.002
INIT_MOTOR_ANGLES = [0, -0.6, 1.4] * 4


class MiniCheetahTest(googletest.TestCase):

  def test_init(self):
    pycram_bullet_client = bullet_client.BulletClient()
    pycram_bullet_client.enable_cns()
    robot = mini_cheetah.MiniCheetah(
        pycram_bullet_client=pycram_bullet_client, time_step=TIME_STEP, on_rack=True)
    self.assertIsNotNone(robot)

  def test_static_pose_on_rack(self):
    pycram_bullet_client = bullet_client.BulletClient()
    pycram_bullet_client.enable_cns()
    pycram_bullet_client.resetSimulation()
    pycram_bullet_client.setPhysicsEngineParameter(numSolverIterations=60)
    pycram_bullet_client.setTimeStep(TIME_STEP)
    pycram_bullet_client.setGravity(0, 0, -10)

    robot = (
        mini_cheetah.MiniCheetah(
            pycram_bullet_client=pycram_bullet_client,
            action_repeat=5,
            time_step=0.002,
            on_rack=True))
    robot.Reset(
        reload_urdf=False,
        default_motor_angles=INIT_MOTOR_ANGLES,
        reset_time=0.5)
    for _ in range(NUM_STEPS):
      robot.Step(INIT_MOTOR_ANGLES)
      motor_angles = robot.GetMotorAngles()
      np.testing.assert_array_almost_equal(
          motor_angles, INIT_MOTOR_ANGLES, decimal=2)


if __name__ == '__main__':
  googletest.main()
