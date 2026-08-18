import sys
import os
import signal
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "commun"))
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "effecteurs"))
import rtde_control
import rtde_receive
from client_mqtt import RobotMqttClient

UR12E_IP = "10.120.0.12"

rtde_c = rtde_control.RTDEControlInterface(UR12E_IP)
rtde_r = rtde_receive.RTDEReceiveInterface(UR12E_IP)

def cleanup(signum=None, frame=None):
    print("Fermeture de la connexion RTDE (ur12e)...")
    rtde_c.disconnect()
    sys.exit(0)

signal.signal(signal.SIGINT, cleanup)
signal.signal(signal.SIGTERM, cleanup)

def move_to_point_b():
    point_b = [-0.5072557911912113, -0.25443998332771245, 0.3574337933610186, -2.8795415568565432, -1.2341722001833153, -0.07000425237093798]
    rtde_c.moveL(point_b, speed=0.1, acceleration=0.1)

def move_to_point_e():
    point_e = [-0.6992066832523436, -0.2544319239003424, 0.3574493183361128, -2.879549786941135, -1.2341247557601733, -0.0699349585606065]
    rtde_c.moveL(point_e, speed=0.1, acceleration=0.1)

TASKS = {
    "move_to_point_b": move_to_point_b,
    "move_to_point_e": move_to_point_e,
}

def handle_task(data):
    task = data.get("task")
    if task in TASKS:
        TASKS[task]()
    else:
        raise ValueError(f"tâche inconnue: {task}")

if __name__ == "__main__":
    client = RobotMqttClient("ur12e")
    client.on_task = handle_task
    client.run_forever()
