from pycram_bullet_utils import bullet_client as bc
from pycram_bullet_utils import urdfEditor as ed
import pycram_bullet
import pycram_bullet_data
import time
import argparse

parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('--urdf_in', help='urdf file name input', default='test.urdf')
parser.add_argument('--urdf_out', help='urdf file name output', default='out.urdf')
parser.add_argument('--urdf_flags', help='urdf flags', type=int, default=0)



args = parser.parse_args()


p0 = bc.BulletClient(connection_mode=pycram_bullet.DIRECT)

p0.setAdditionalSearchPath(pycram_bullet_data.getDataPath())
body_id = p0.loadURDF(args.urdf_in, flags = args.urdf_flags)
ed0 = ed.UrdfEditor()
ed0.initializeFromBulletBody(body_id, p0._client)
ed0.saveUrdf(args.urdf_out)

