from pycram_bullet_utils import bullet_client as bc
import pycram_bullet
import pycram_bullet_data

p0 = bc.BulletClient(connection_mode=pycram_bullet.DIRECT)
p0.setAdditionalSearchPath(pycram_bullet_data.getDataPath())

p1 = bc.BulletClient(connection_mode=pycram_bullet.DIRECT)
p1.setAdditionalSearchPath(pycram_bullet_data.getDataPath())

#can also connect using different modes, GUI, SHARED_MEMORY, TCP, UDP, SHARED_MEMORY_SERVER, GUI_SERVER
#pgui = bc.BulletClient(connection_mode=pycram_bullet.GUI)

p0.loadURDF("r2d2.urdf")
p1.loadSDF("stadium.sdf")
print(p0._client)
print(p1._client)
print("p0.getNumBodies()=", p0.getNumBodies())
print("p1.getNumBodies()=", p1.getNumBodies())
