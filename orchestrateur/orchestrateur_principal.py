import json
import paho.mqtt.client as mqtt
from machine_etats import OrchestratorCellule

COURTIER = "localhost"
orchestrateur = OrchestratorCellule()

CMD_TOPICS = {
    "ur5_vers_a":   ("cell/robot/ur5/cmd",   {"task": "cycle_pose_bride"}),
    "ur12e_vers_b": ("cell/robot/ur12e/cmd", {"task": "cycle_vissage_bride"}),
    "ur5_vers_c":  ("cell/robot/ur5/cmd",  {"task": "cycle_pose_sup_pico"}),
    "ur12e_vers_d":   ("cell/robot/ur12e/cmd",   {"task": "cycle_vissage_sup_pico"}),
    "ur5_vers_e": ("cell/robot/ur5/cmd", {"task": "cycle_pose_sup_l298N"}),
    "ur12e_vers_f":  ("cell/robot/ur12e/cmd",  {"task": "cycle_vissage_sup_l298n"}),
    "ur5_vers_j":  ("cell/robot/ur5/cmd",  {"task": "cycle_pose_carte_l298N"}),
}

NEXT_TRANSITION = {
    ("ur5", "ur5_vers_a"):     "a_reached",
    ("ur12e", "ur12e_vers_b"): "b_reached",
    ("ur5", "ur5_vers_c"):   "c_reached",
    ("ur12e", "ur12e_vers_d"):     "d_reached",
    ("ur5", "ur5_vers_e"): "e_reached",
    ("ur12e", "ur12e_vers_f"):   "f_reached",
    ("ur5", "ur5_vers_j"): "j_reached",
}

def nettoyer_messages_retenus(client):
    """Efface tous les messages retenus en publiant des messages vides."""
    for state, (topic, _) in CMD_TOPICS.items():
        client.publish(topic, "", retain=True)
    print("[INIT] Messages retenus effacés")

def publish_current_task(client):
    if orchestrateur.state in CMD_TOPICS:
        topic, payload = CMD_TOPICS[orchestrateur.state]
        client.publish(topic, json.dumps(payload), retain=False)
        print(f"-> {topic}: {payload}")
    elif orchestrateur.state == "done":
        print("Cycle terminé.")

def on_connect(client, userdata, flags, rc):
    print("Connecté au broker, code:", rc)
    client.subscribe("cell/robot/+/status")
    nettoyer_messages_retenus(client) 
    orchestrateur.start()
    publish_current_task(client)

def on_message(client, userdata, msg):
    data = json.loads(msg.payload.decode())
    robot = msg.topic.split("/")[2]
    print(f"<- {msg.topic}: {data}")

    if data.get("state") != "done":
        return

    key = (robot, orchestrateur.state)
    if key in NEXT_TRANSITION:
        trigger = NEXT_TRANSITION[key]
        getattr(orchestrateur, trigger)()
        publish_current_task(client)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(COURTIER, 1883, 60)
client.loop_forever()

