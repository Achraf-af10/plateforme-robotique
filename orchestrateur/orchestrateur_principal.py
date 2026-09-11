import os
import json
import paho.mqtt.client as mqtt
from machine_etats import OrchestratorCellule

COURTIER = "localhost"

ETAT_DEPART = os.environ.get("ETAT_DEPART", "idle")
MODE_PAS_A_PAS = os.environ.get("PAS_A_PAS", "0") == "1"

orchestrateur = OrchestratorCellule()

if ETAT_DEPART != "idle":
    if ETAT_DEPART not in orchestrateur.states:
        raise ValueError(f"ETAT_DEPART invalide : '{ETAT_DEPART}'. "
                          f"Valeurs possibles : {orchestrateur.states}")
    orchestrateur.machine.set_state(ETAT_DEPART)
    print(f"[TEST] Démarrage forcé à l'état : {ETAT_DEPART}")

CMD_TOPICS = {
    "ur12e_vers_a": ("cell/robot/ur12e/cmd", {"task": "cycle_vissage_entretoises_pico"}),
    "ur12e_vers_b": ("cell/robot/ur12e/cmd", {"task": "cycle_vissage_entretoises_l298n"}),
    "ur5_vers_1":   ("cell/robot/ur5/cmd",   {"task": "cycle_pose_bride"}),
    "ur12e_vers_2": ("cell/robot/ur12e/cmd", {"task": "cycle_vissage_bride"}),
    "ur5_vers_3":   ("cell/robot/ur5/cmd",   {"task": "cycle_pose_sup_pico"}),
    "ur12e_vers_4": ("cell/robot/ur12e/cmd", {"task": "cycle_vissage_sup_pico"}),
    "ur5_vers_5":   ("cell/robot/ur5/cmd",   {"task": "cycle_pose_sup_l298N"}),
    "ur12e_vers_6": ("cell/robot/ur12e/cmd", {"task": "cycle_vissage_sup_l298n"}),
    "ur12e_vers_8": ("cell/robot/ur12e/cmd", {"task": "cycle_vissage_entretoises_raspi"}),
    "ur5_vers_9":   ("cell/robot/ur5/cmd",   {"task": "cycle_pose_sup1_raspi"}),
    "ur12e_vers_10": ("cell/robot/ur12e/cmd", {"task": "cycle_vissage_sup1_raspi"}),
    "ur5_vers_11":   ("cell/robot/ur5/cmd",   {"task": "cycle_pose_sup2_raspi"}),
    "ur12e_vers_12": ("cell/robot/ur12e/cmd", {"task": "cycle_vissage_sup2_raspi"}),
    "ur5_vers_13":   ("cell/robot/ur5/cmd",   {"task": "cycle_pose_sup_powerbank"}),
    "ur12e_vers_14": ("cell/robot/ur12e/cmd", {"task": "cycle_vissage_sup_powerbank"}),
}

NEXT_TRANSITION = {
    ("ur12e", "ur12e_vers_a"): "a_reached",
    ("ur12e", "ur12e_vers_b"): "b_reached",
    ("ur5", "ur5_vers_1"):     "1_reached",
    ("ur12e", "ur12e_vers_2"): "2_reached",
    ("ur5", "ur5_vers_3"):     "3_reached",
    ("ur12e", "ur12e_vers_4"): "4_reached",
    ("ur5", "ur5_vers_5"):     "5_reached",
    ("ur12e", "ur12e_vers_6"): "6_reached",
    ("ur12e", "ur12e_vers_8"): "8_reached",
    ("ur5", "ur5_vers_9"):     "9_reached",
    ("ur12e", "ur12e_vers_10"): "10_reached",
    ("ur5", "ur5_vers_11"):     "11_reached",
    ("ur12e", "ur12e_vers_12"): "12_reached",
    ("ur5", "ur5_vers_13"):     "13_reached",
    ("ur12e", "ur12e_vers_14"): "14_reached",
}

ETATS_AVEC_PAUSE = {
    "ur5_vers_1",   # changement outil de visseuse
    "ur5_vers_9",   # changement outil de visseuse
    "ur12e_vers_8", # retourner la plateforme pour visser les entretoises du raspi
}

def nettoyer_messages_retenus(client):
    for state, (topic, _) in CMD_TOPICS.items():
        client.publish(topic, "", retain=True)

def attendre_confirmation():
    print(f"\n[PAUSE] Prochaine étape : {orchestrateur.state}")
    input("        Appuie sur Entrée pour continuer...")

def publish_current_task(client):
    if orchestrateur.state in CMD_TOPICS:
        if MODE_PAS_A_PAS and orchestrateur.state in ETATS_AVEC_PAUSE:
            attendre_confirmation()
        topic, payload = CMD_TOPICS[orchestrateur.state]
        client.publish(topic, json.dumps(payload), retain=False)
        print(f"-> {topic}: {payload}")
    elif orchestrateur.state == "done":
        print("Cycle terminé.")

premiere_connexion = True

def on_connect(client, userdata, flags, rc):
    global premiere_connexion
    print("Connecté au broker, code:", rc)
    client.subscribe("cell/robot/+/status")

    if premiere_connexion:
        nettoyer_messages_retenus(client)
        if ETAT_DEPART == "idle":
            orchestrateur.start()
        publish_current_task(client)
        premiere_connexion = False
    else:
        print("[RECONNEXION] Pas de republication, on continue où on en était.")

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