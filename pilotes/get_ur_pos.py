from rtde_receive import RTDEReceiveInterface
from rtde_control import RTDEControlInterface


rtde_r_ur5 = RTDEReceiveInterface("10.120.0.11")
rtde_c_ur5 = RTDEControlInterface("10.120.0.11")

if rtde_r_ur5.isConnected():
    print("Connexion OKKK")
    
    print(f"Position joints UR5: {rtde_r_ur5.getActualQ()}") # rad
    print(f"Position TCP UR5: {rtde_r_ur5.getActualTCPPose()}") # xyz m + rpy rad

else:
    print("Echec connexion UR5")

rtde_r_ur12e = RTDEReceiveInterface("10.120.0.12")
rtde_c_ur12e = RTDEControlInterface("10.120.0.12")

print("=========================================")
if rtde_r_ur12e.isConnected():
    print("Connexion OKKK")
    
    print(f"Position joints UR12e: {rtde_r_ur12e.getActualQ()}") # rad
    print(f"Position TCP UR12e: {rtde_r_ur12e.getActualTCPPose()}") # xyz m + rpy rad

else:
    print("Echec connexion UR12e")