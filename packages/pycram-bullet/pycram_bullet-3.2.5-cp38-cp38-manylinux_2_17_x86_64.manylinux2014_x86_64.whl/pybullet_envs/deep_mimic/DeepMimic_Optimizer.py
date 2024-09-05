import numpy as np
import sys
import os
import inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(os.path.dirname(currentdir))
os.sys.path.insert(0, parentdir)
print("parentdir=", parentdir)

from pycram_bullet_envs.deep_mimic.env.pycram_bullet_deep_mimic_env import PyBulletDeepMimicEnv
from pycram_bullet_envs.deep_mimic.learning.rl_world import RLWorld
from pycram_bullet_utils.logger import Logger
from pycram_bullet_envs.deep_mimic.testrl import update_world, update_timestep, build_world
import pycram_bullet_utils.mpi_util as MPIUtil

args = []
world = None


def run():
  global update_timestep
  global world
  done = False
  while not (done):
    update_world(world, update_timestep)

  return


def shutdown():
  global world

  Logger.print2('Shutting down...')
  world.shutdown()
  return


def main():
  global args
  global world

  # Command line arguments
  args = sys.argv[1:]
  enable_draw = False
  world = build_world(args, enable_draw)

  run()
  shutdown()

  return


if __name__ == '__main__':
  main()
