from rtde_receive import RTDEReceiveInterface

# fonction test pour recuperer la position des robots UR5 et UR12e

# --- UR5 ---
try:
    ur5 = RTDEReceiveInterface("10.120.0.11")
    print(f"[UR5]  Joints: {ur5.getActualQ()}\n[UR5]  TCP:    {ur5.getActualTCPPose()}")
    ur5.disconnect()
except:
    print("[UR5]  Erreur de connexion")

print("#######################")
# --- UR12e ---
try:
    ur12e = RTDEReceiveInterface("10.120.0.12")
    print(f"[UR12e] Joints: {ur12e.getActualQ()}\n[UR12e] TCP:    {ur12e.getActualTCPPose()}")
    ur12e.disconnect()
except:
    print("[UR12e] Erreur de connexion")
