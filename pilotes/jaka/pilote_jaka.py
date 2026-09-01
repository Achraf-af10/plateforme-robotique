"""
Pilote JAKA : gère la communication MQTT et délègue aux scenarios.
Responsabilité : orchestration MQTT uniquement.
"""
import sys
import os
import signal
import jkrc

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "commun"))
sys.path.insert(0, os.path.dirname(__file__))

from client_mqtt import RobotMqttClient
from scenarios_jaka import pick_and_place

# Initialiser la connexion au robot
robot = jkrc.RC("10.120.0.13")
if robot.login()[0] != 0:
    print("[jaka] Erreur connexion")
    sys.exit(1)

robot.power_on()
robot.enable_robot()
print("[jaka] Connecté")

def cleanup(signum=None, frame=None):
    """Fermeture propre."""
    print("[jaka] Fermeture connexion...")
    robot.logout()
    sys.exit(0)

signal.signal(signal.SIGINT, cleanup)
signal.signal(signal.SIGTERM, cleanup)

# Définir les tâches disponibles
TASKS = {
    "cycle_pose_sup_pico": lambda data: pick_and_place(robot),
}

def handle_task(data):
    """Callback MQTT : exécuter la tâche demandée."""
    task = data.get("task")
    if task in TASKS:
        try:
            TASKS[task](data)
        except Exception as e:
            print(f"[jaka] Erreur tâche {task} : {e}")
            raise
    else:
        raise ValueError(f"Tâche inconnue: {task}")

if __name__ == "__main__":
    client = RobotMqttClient("jaka")
    client.on_task = handle_task
    client.run_forever()