import sys
import os
import signal

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "commun"))
sys.path.append(os.path.dirname(__file__)) 

import rtde_control
import rtde_receive
from client_mqtt import RobotMqttClient
from scenarios_ur5 import prendre_support_L298N 

UR5_IP = "10.120.0.11"

rtde_c = rtde_control.RTDEControlInterface(UR5_IP)
rtde_r = rtde_receive.RTDEReceiveInterface(UR5_IP)

def cleanup(signum=None, frame=None):
    print("Fermeture de la connexion RTDE (ur5)...")
    rtde_c.disconnect()
    sys.exit(0)

signal.signal(signal.SIGINT, cleanup)
signal.signal(signal.SIGTERM, cleanup)

def move_to_point_a(data):
    prendre_support_L298N(rtde_c, rtde_r, data)

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
        fonction = TASKS[task]
        # Les taches qui ont besoin de "data" (ex: numero de piece) le recoivent ;
        # les autres (move_to_point_a/d) ne prennent aucun argument.
        if fonction.__code__.co_argcount == 1:
            fonction(data)
        else:
            fonction()
    else:
        raise ValueError(f"tâche inconnue: {task}")

if __name__ == "__main__":
    client = RobotMqttClient("ur5")
    client.on_task = handle_task
    client.run_forever()