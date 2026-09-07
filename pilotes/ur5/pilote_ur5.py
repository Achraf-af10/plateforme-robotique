"""
Pilote UR5 : gère la communication MQTT et délègue à UR5 + scenarios.
Responsabilité : orchestration MQTT uniquement.
"""
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "commun"))
sys.path.insert(0, os.path.dirname(__file__))

from client_mqtt import RobotMqttClient
from ur5_robot import UR5
from scenarios_ur5 import cycle_pose, cycle_pose_grille
import config_ur5

# Initialiser le robot
robot = UR5(ip="10.120.0.11")

# Définir les tâches disponibles
TASKS = {
    "cycle_pose_bride": lambda data: cycle_pose_grille(robot, grille=config_ur5.BRIDE_MOTEUR),
    "cycle_pose_sup_pico": lambda data: cycle_pose(robot, support_list=[config_ur5.SUPPORT_PICO]),
    "cycle_pose_sup_l298N": lambda data: cycle_pose(robot, support_list=[config_ur5.SUPPORT_L298N]),
    "cycle_pose_carte_l298N": lambda data: cycle_pose(robot, support_list=[config_ur5.CARTE_L298N]),
    "cycle_pose_sup1_raspi": lambda data: cycle_pose(robot, support_list=[config_ur5.SUPPORT_SUP1_RASPI]),
    "cycle_pose_sup2_raspi": lambda data: cycle_pose(robot, support_list=[config_ur5.SUPPORT_SUP2_RASPI]),

}

def handle_task(data):
    """Callback MQTT : exécuter la tâche demandée."""
    task = data.get("task")
    if task in TASKS:
        try:
            TASKS[task](data)
        except Exception as e:
            print(f"[ur5] Erreur tâche {task} : {e}")
            raise
    else:
        raise ValueError(f"Tâche inconnue: {task}")

if __name__ == "__main__":
    client = RobotMqttClient("ur5")
    client.on_task = handle_task
    client.run_forever()
