"""
Pilote UR12e : gère la communication MQTT et délègue à UR12e + scenarios.
Responsabilité : orchestration MQTT uniquement.
"""
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "commun"))
sys.path.insert(0, os.path.dirname(__file__))

from client_mqtt import RobotMqttClient
from ur12e_robot import UR12e
from scenarios_ur12e import cycle_vissage, cycle_vissage_grille
import config_ur12e

# Initialiser le robot
robot = UR12e(ip="10.120.0.12")

# Définir les tâches disponibles
TASKS = {
    "cycle_vissage_bride": lambda data: cycle_vissage_grille(robot,vis_list=config_ur12e.VIS_BRIDE_MOTEUR, grille=config_ur12e.GRILLE_VIS_8X8),
    "cycle_vissage_sup_pico": lambda data: cycle_vissage(robot,vis_list=config_ur12e.VIS_SUP_PICO),
    "cycle_vissage_sup_l298n": lambda data: cycle_vissage(robot,vis_list=config_ur12e.VIS_SUP_L298N),
}

def handle_task(data):
    """Callback MQTT : exécuter la tâche demandée."""
    task = data.get("task")
    if task in TASKS:
        try:
            TASKS[task](data)
        except Exception as e:
            print(f"[ur12e] Erreur tâche {task} : {e}")
            raise
    else:
        raise ValueError(f"Tâche inconnue: {task}")

if __name__ == "__main__":
    client = RobotMqttClient("ur12e")
    client.on_task = handle_task
    client.run_forever()
