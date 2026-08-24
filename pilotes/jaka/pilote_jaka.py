import sys
import os
import signal
import time
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "commun"))
import jkrc
from client_mqtt import RobotMqttClient

JAKA_IP = "10.120.0.13"

robot = jkrc.RC(JAKA_IP)
robot.login()
robot.power_on()
robot.enable_robot()

def cleanup(signum=None, frame=None):
    print("Fermeture de la connexion JAKA...")
    robot.logout()
    sys.exit(0)

signal.signal(signal.SIGINT, cleanup)
signal.signal(signal.SIGTERM, cleanup)

        
def move_to_point_c():
    point_c = [1.7388542253407, 1.2955673064333557, 1.5242288219560445, 1.8926079559748334, -1.5707928093415555, 3.3096465110834887]
    robot.joint_move(point_c, 0, True, 1.0)
    point_f = [1.4738710124401888, 1.3598507487474776, 2.1521663365868333, 1.2003992163344779, -1.5707928093415555, 3.044663298182978]
    robot.joint_move(point_f, 0, True, 1.0)
    point_c = [1.7388542253407, 1.2955673064333557, 1.5242288219560445, 1.8926079559748334, -1.5707928093415555, 3.3096465110834887]
    robot.joint_move(point_c, 0, True, 1.0)
def move_to_point_f():
    point_f = [1.4738710124401888, 1.3598507487474776, 2.1521663365868333, 1.2003992163344779, -1.5707928093415555, 3.044663298182978]
    robot.joint_move(point_f, 0, True, 1.0)
TASKS = {
    "move_to_point_c": move_to_point_c,
    "move_to_point_f": move_to_point_f,
}

def handle_task(data):
    task = data.get("task")
    if task in TASKS:
        TASKS[task]()
    else:
        raise ValueError(f"tâche inconnue: {task}")

if __name__ == "__main__":
    client = RobotMqttClient("jaka")
    client.on_task = handle_task
    client.run_forever()