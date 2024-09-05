import os
import inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(os.path.dirname(currentdir))
os.sys.path.insert(0, parentdir)

import pycram_bullet as p
import pycram_bullet_data
import time


def test(args):
  p.connect(p.GUI)
  p.setAdditionalSearchPath(pycram_bullet_data.getDataPath())
  fileName = os.path.join("mjcf", args.mjcf)
  print("fileName")
  print(fileName)
  p.loadMJCF(fileName)
  while (1):
    p.stepSimulation()
    p.getCameraImage(320, 240)
    time.sleep(0.01)


if __name__ == '__main__':
  import argparse
  parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
  parser.add_argument('--mjcf', help='MJCF filename', default="humanoid.xml")
  args = parser.parse_args()
  test(args)
