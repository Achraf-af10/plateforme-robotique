import jkrc
import paho.mqtt.client as mqtt
import json
import time
import os
import subprocess

COURTIER_IP   = "127.0.0.1"
COURTIER_PORT = 1883
FREQUENCE     = 1  # Hz

NOM = "jaka"
IP   = "10.120.0.13"

JAKA_JOINTS = ["J1", "J2", "J3", "J4", "J5", "J6"]
FICHIER_ENERGIE = "energie_cumulee_jaka.json"
SAUVEGARDER_TOUS_LES_N_CYCLES = 10
PING_TIMEOUT = 1


def joignable(ip, timeout=PING_TIMEOUT):
    try:
        result = subprocess.run(
            ["ping", "-c", "1", "-W", str(timeout), ip],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        return result.returncode == 0
    except Exception:
        return False


def charger_energie():
    if os.path.exists(FICHIER_ENERGIE):
        try:
            with open(FICHIER_ENERGIE, "r") as f:
                data = json.load(f)
                print(f"[INFO] Énergie cumulée rechargée : {data}")
                return data.get(NOM, 0.0)
        except Exception as e:
            print(f"[ERREUR] Lecture {FICHIER_ENERGIE} impossible ({e}), reset à 0")
    return 0.0


def sauvegarder_energie(energie):
    try:
        with open(FICHIER_ENERGIE, "w") as f:
            json.dump({NOM: energie}, f)
    except Exception as e:
        print(f"[ERREUR] Sauvegarde {FICHIER_ENERGIE} impossible : {e}")


def connecter_robot():
    try:
        robot = jkrc.RC(IP)
        robot.login()
        robot.power_on()
        time.sleep(8)
        robot.enable_robot()
        print(f"[OK] Connecté à {NOM} ({IP})")
        return robot
    except Exception as e:
        print(f"[ERREUR] Impossible de se connecter à {NOM} ({IP}) : {e}")
        return None


def deconnecter_robot(robot):
    try:
        robot.logout()
        print(f"[OK] Déconnexion propre de {NOM}")
    except Exception as e:
        print(f"[ERREUR] Déconnexion {NOM} : {e}")


def publier_donnees_robot(client, robot, energie_cumulee, dt):
    if not joignable(IP):
        client.publish(f"{NOM}/state", json.dumps({
            "connected": False,
            "energie": round(energie_cumulee, 3),
        }))
        print(f"[AVERTISSEMENT] {NOM} injoignable ({IP}) — énergie gelée, pas de lecture")
        return energie_cumulee

    ret = robot.get_robot_status()
    if ret[0] != 0:
        raise RuntimeError(f"get_robot_status a renvoyé le code {ret[0]}")

    monitor = ret[1][20]
    tension_v  = monitor[0] / 1000.0
    courant_a  = monitor[1] / 1000.0
    joints_raw = monitor[5]

    puissance = tension_v * courant_a
    energie_cumulee += puissance * (dt / 3600)

    state = {
        "connected": True,
        "current":   round(courant_a, 3),
        "voltage":   round(tension_v, 3),
        "puissance": round(puissance, 3),
        "energie":   round(energie_cumulee, 3),
    }
    client.publish(f"{NOM}/state", json.dumps(state))

    joints = {}
    for i, j in enumerate(joints_raw):
        joints[JAKA_JOINTS[i]] = {
            "current":     round(j[0], 4),
            "voltage":     round(j[1], 1),
            "temperature": round(j[2], 1),
            "puissance":   round(j[0] * j[1], 3),
        }
    client.publish(f"{NOM}/joints", json.dumps(joints))

    return energie_cumulee


def main():
    robot = connecter_robot()
    if robot is None:
        print("JAKA injoignable, arrêt du script.")
        return

    energie_cumulee = charger_energie()

    client = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2)
    client.connect(COURTIER_IP, COURTIER_PORT)
    client.loop_start()
    print("Publication MQTT (JAKA) démarrée...")

    last_time = time.time()
    cycle_count = 0

    try:
        while True:
            now = time.time()
            dt = now - last_time
            last_time = now

            try:
                energie_cumulee = publier_donnees_robot(client, robot, energie_cumulee, dt)
            except Exception as e:
                print(f"[ERREUR] Lecture/publication {NOM} : {e}")

            cycle_count += 1
            if cycle_count >= SAUVEGARDER_TOUS_LES_N_CYCLES:
                sauvegarder_energie(energie_cumulee)
                cycle_count = 0

            time.sleep(1 / FREQUENCE)

    except KeyboardInterrupt:
        print("Arrêt")
    finally:
        sauvegarder_energie(energie_cumulee)
        deconnecter_robot(robot)
        client.loop_stop()
        client.disconnect()


if __name__ == "__main__":
    main()
