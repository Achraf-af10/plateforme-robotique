import os
import subprocess
import sys
import signal
import time

# Répertoire du script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Python utilisé pour le JAKA
PYTHON_JAKA = os.path.join(BASE_DIR, "venv_jaka", "bin", "python")

# Scripts de télémétrie à lancer
SCRIPTS = ["ur5_telemetrie.py", "ur12e_telemetrie.py", "jaka_telemetrie.py"]

# Liste des processus lancés
processes = []


def arreter_tous(signum=None, frame=None):
    # Arrête tous les scripts
    print("\nArrêt de tous les scripts de télémétrie...")
    for name, p in processes:
        p.send_signal(signal.SIGINT)

    # Attend leur arrêt
    for name, p in processes:
        p.wait(timeout=10)
        print(f"[OK] {name} arrêté")

    sys.exit(0)


def main():
    # Gère l'arrêt avec Ctrl+C ou SIGTERM
    signal.signal(signal.SIGINT, arreter_tous)
    signal.signal(signal.SIGTERM, arreter_tous)

    # Lance chaque script
    for script in SCRIPTS:
        # Utilise l'environnement Python du JAKA
        if script == "jaka_telemetrie.py":
            python_bin = PYTHON_JAKA
        else:
            python_bin = sys.executable

        # Lance le processus
        p = subprocess.Popen([python_bin, script], cwd=BASE_DIR)

        # Ajoute le processus à la liste
        processes.append((script, p))
        print(f"[OK] {script} lancé (pid={p.pid}) avec {python_bin}")

    try:
        # Surveille les processus
        while True:
            for name, p in processes:
                if p.poll() is not None:
                    print(f"[AVERTISSEMENT] {name} s'est arrêté (code {p.returncode})")

            # Vérifie toutes les 2 secondes
            time.sleep(2)

    except KeyboardInterrupt:
        arreter_tous()


if __name__ == "__main__":
    # Lance le programme principal
    main()