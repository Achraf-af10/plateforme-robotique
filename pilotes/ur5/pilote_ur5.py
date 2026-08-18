import sys
import os
import signal
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "commun"))
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "effecteurs"))
import rtde_control
import rtde_receive
from client_mqtt import RobotMqttClient

UR5_IP = "10.120.0.11"

rtde_c = rtde_control.RTDEControlInterface(UR5_IP)
rtde_r = rtde_receive.RTDEReceiveInterface(UR5_IP)

def cleanup(signum=None, frame=None):
    print("Fermeture de la connexion RTDE (ur5)...")
    rtde_c.disconnect()
    sys.exit(0)

signal.signal(signal.SIGINT, cleanup)
signal.signal(signal.SIGTERM, cleanup)

def move_to_point_a():
    point_a = [0.48187679988574483, -0.1451834444286808, 0.40351652871902666, -2.289334219663615, 2.0242017706495314, -0.11342767788255038]
    rtde_c.moveL(point_a, speed=0.1, acceleration=0.1)

def move_to_point_d():
    point_d = [0.48196370064505684, 0.12043598350031744, 0.40348327636507847, -2.2894946260793576, 2.024437833830858, -0.11439462567385185]
    rtde_c.moveL(point_d, speed=0.1, acceleration=0.1)

TASKS = {
    "move_to_point_a": move_to_point_a,
    "move_to_point_d": move_to_point_d,
}

def handle_task(data):
    task = data.get("task")
    if task in TASKS:
        TASKS[task]()
    else:
        raise ValueError(f"tâche inconnue: {task}")

if __name__ == "__main__":
    client = RobotMqttClient("ur5")
    client.on_task = handle_task
    client.run_forever()