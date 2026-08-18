import rtde_control
import rtde_receive

from ur5.scenarios_ur5 import prendre_support_L298N, initialiser_pile_L298N

ROBOT_IP = "10.120.0.11"

rtde_c = rtde_control.RTDEControlInterface(ROBOT_IP)
rtde_r = rtde_receive.RTDEReceiveInterface(ROBOT_IP)

# Initialiser la pile
initialiser_pile_L298N(5)

# Support à prendre
data = {"numero": 1}

# Lancer le test
prendre_support_L298N(rtde_c, rtde_r, data)

rtde_c.stopScript()