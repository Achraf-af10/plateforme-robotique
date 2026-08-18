from rtde_receive import RTDEReceiveInterface
import paho.mqtt.client as mqtt
import json
import time
import os

COURTIER_IP   = "127.0.0.1"
COURTIER_PORT = 1883
FREQUENCE     = 1  # Hz

JOINTS = ["J1", "J2", "J3", "J4", "J5", "J6"]
SAUVEGARDER_TOUS_LES_N_CYCLES = 10


def charger_energie(fichier_energie, nom_robot):
    if os.path.exists(fichier_energie):
        try:
            with open(fichier_energie, "r") as f:
                data = json.load(f)
                print(f"[INFO] Énergie cumulée rechargée : {data}")
                return data.get(nom_robot, 0.0)
        except Exception as e:
            print(f"[ERREUR] Lecture {fichier_energie} impossible ({e}), reset à 0")
    return 0.0


def sauvegarder_energie(fichier_energie, nom_robot, energie):
    try:
        with open(fichier_energie, "w") as f:
            json.dump({nom_robot: energie}, f)
    except Exception as e:
        print(f"[ERREUR] Sauvegarde {fichier_energie} impossible : {e}")


def connecter_robot(nom, ip):
    try:
        rtde_r = RTDEReceiveInterface(ip)
        print(f"[OK] Connecté à {nom} ({ip})")
        return rtde_r
    except Exception as e:
        print(f"[ERREUR] Impossible de se connecter à {nom} ({ip}) : {e}")
        return None


def publier_donnees_robot(client, nom, rtde_r, energie_cumulee, dt):
    """Retourne l'énergie cumulée mise à jour."""
    if not rtde_r.isConnected():
        client.publish(f"{nom}/state", json.dumps({
            "connected": False,
            "energie_cumulee_wh": round(energie_cumulee, 3),
        }))
        print(f"[AVERTISSEMENT] {nom} déconnecté (RTDE) — énergie gelée, pas de lecture")
        return energie_cumulee

    current      = rtde_r.getActualRobotCurrent()
    voltage      = rtde_r.getActualRobotVoltage()
    currents     = rtde_r.getActualCurrent()
    voltages     = rtde_r.getActualJointVoltage()
    temperatures = rtde_r.getJointTemperatures()

    puissance = current * voltage
    energie_cumulee += puissance * (dt / 3600)

    state = {
        "connected": True,
        "current":   round(current, 3),
        "voltage":   round(voltage, 3),
        "puissance": round(puissance, 3),
        "energie":   round(energie_cumulee, 3),
    }
    client.publish(f"{nom}/state", json.dumps(state))

    joints = {
        joint: {
            "current":     round(currents[i], 3),
            "voltage":     round(voltages[i], 3),
            "temperature": round(temperatures[i], 2),
            "puissance":   round(currents[i] * voltages[i], 3),
        }
        for i, joint in enumerate(JOINTS)
    }
    client.publish(f"{nom}/joints", json.dumps(joints))

    return energie_cumulee


def lancer_telemetrie_ur(nom, ip, fichier_energie):
    """Boucle principale générique pour UR5 et UR12e."""
    rtde_r = connecter_robot(nom, ip)
    if rtde_r is None:
        print(f"{nom} injoignable, arrêt du script.")
        return

    energie_cumulee = charger_energie(fichier_energie, nom)

    client = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2)
    client.connect(COURTIER_IP, COURTIER_PORT)
    client.loop_start()
    print(f"Publication MQTT ({nom}) démarrée...")

    last_time = time.time()
    cycle_count = 0

    try:
        while True:
            now = time.time()
            dt = now - last_time
            last_time = now

            try:
                energie_cumulee = publier_donnees_robot(client, nom, rtde_r, energie_cumulee, dt)
            except Exception as e:
                print(f"[ERREUR] Lecture/publication {nom} : {e}")

            cycle_count += 1
            if cycle_count >= SAUVEGARDER_TOUS_LES_N_CYCLES:
                sauvegarder_energie(fichier_energie, nom, energie_cumulee)
                cycle_count = 0

            time.sleep(1 / FREQUENCE)

    except KeyboardInterrupt:
        print(f"Arrêt {nom}")
    finally:
        sauvegarder_energie(fichier_energie, nom, energie_cumulee)
        client.loop_stop()
        client.disconnect()
