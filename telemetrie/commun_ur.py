from rtde_receive import RTDEReceiveInterface
import paho.mqtt.client as mqtt
import json
import time
import os

# Configuration MQTT
COURTIER_IP   = "127.0.0.1"
COURTIER_PORT = 1883
FREQUENCE     = 1  # Hz

# Noms des articulations
JOINTS = ["J1", "J2", "J3", "J4", "J5", "J6"]

# Sauvegarde de l'énergie tous les N cycles
SAUVEGARDER_TOUS_LES_N_CYCLES = 10


def charger_energie(fichier_energie, nom_robot):
    # Vérifie si le fichier existe
    if os.path.exists(fichier_energie):
        try:
            # Charge l'énergie sauvegardée
            with open(fichier_energie, "r") as f:
                data = json.load(f)
                print(f"[INFO] Énergie cumulée rechargée : {data}")
                return data.get(nom_robot, 0.0)
        except Exception as e:
            print(f"[ERREUR] Lecture {fichier_energie} impossible ({e}), reset à 0")
    return 0.0


def sauvegarder_energie(fichier_energie, nom_robot, energie):
    try:
        # Sauvegarde l'énergie dans le fichier JSON
        with open(fichier_energie, "w") as f:
            json.dump({nom_robot: energie}, f)
    except Exception as e:
        print(f"[ERREUR] Sauvegarde {fichier_energie} impossible : {e}")


def connecter_robot(nom, ip):
    try:
        # Connexion au robot via RTDE
        rtde_r = RTDEReceiveInterface(ip)
        print(f"[OK] Connecté à {nom} ({ip})")
        return rtde_r
    except Exception as e:
        print(f"[ERREUR] Impossible de se connecter à {nom} ({ip}) : {e}")
        return None


def publier_donnees_robot(client, nom, rtde_r, energie_cumulee, dt):
    """Retourne l'énergie cumulée mise à jour."""

    # Vérifie la connexion au robot
    if not rtde_r.isConnected():
        client.publish(f"{nom}/state", json.dumps({
            "connected": False,
            "energie_cumulee_wh": round(energie_cumulee, 3),
        }))
        print(f"[AVERTISSEMENT] {nom} déconnecté (RTDE) — énergie gelée, pas de lecture")
        return energie_cumulee

    # Récupère les mesures du robot
    current      = rtde_r.getActualRobotCurrent()
    voltage      = rtde_r.getActualRobotVoltage()
    currents     = rtde_r.getActualCurrent()
    voltages     = rtde_r.getActualJointVoltage()
    temperatures = rtde_r.getJointTemperatures()

    # Calcule la puissance et l'énergie
    puissance = current * voltage
    energie_cumulee += puissance * (dt / 3600)

    # Prépare les données générales du robot
    state = {
        "connected": True,
        "current":   round(current, 3),
        "voltage":   round(voltage, 3),
        "puissance": round(puissance, 3),
        "energie":   round(energie_cumulee, 3),
    }

    # Publie l'état du robot sur MQTT
    client.publish(f"{nom}/state", json.dumps(state))

    # Prépare les données de chaque articulation
    joints = {
        joint: {
            "current":     round(currents[i], 3),
            "voltage":     round(voltages[i], 3),
            "temperature": round(temperatures[i], 2),
            "puissance":   round(currents[i] * voltages[i], 3),
        }
        for i, joint in enumerate(JOINTS)
    }

    # Publie les données des articulations sur MQTT
    client.publish(f"{nom}/joints", json.dumps(joints))

    return energie_cumulee


def lancer_telemetrie_ur(nom, ip, fichier_energie):
    """Boucle principale générique pour UR5 et UR12e."""

    # Connexion au robot
    rtde_r = connecter_robot(nom, ip)
    if rtde_r is None:
        print(f"{nom} injoignable, arrêt du script.")
        return

    # Recharge l'énergie précédente
    energie_cumulee = charger_energie(fichier_energie, nom)

    # Connexion au broker MQTT
    client = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2)
    client.connect(COURTIER_IP, COURTIER_PORT)
    client.loop_start()
    print(f"Publication MQTT ({nom}) démarrée...")

    # Initialise le temps et le compteur
    last_time = time.time()
    cycle_count = 0

    try:
        # Boucle de télémétrie
        while True:
            now = time.time()
            dt = now - last_time
            last_time = now

            try:
                # Lit et publie les données du robot
                energie_cumulee = publier_donnees_robot(client, nom, rtde_r, energie_cumulee, dt)
            except Exception as e:
                print(f"[ERREUR] Lecture/publication {nom} : {e}")

            # Compte les cycles
            cycle_count += 1

            # Sauvegarde périodiquement l'énergie
            if cycle_count >= SAUVEGARDER_TOUS_LES_N_CYCLES:
                sauvegarder_energie(fichier_energie, nom, energie_cumulee)
                cycle_count = 0

            # Attend avant le prochain cycle
            time.sleep(1 / FREQUENCE)

    except KeyboardInterrupt:
        print(f"Arrêt {nom}")
    finally:
        # Sauvegarde finale de l'énergie
        sauvegarder_energie(fichier_energie, nom, energie_cumulee)

        # Ferme la connexion MQTT
        client.loop_stop()
        client.disconnect()