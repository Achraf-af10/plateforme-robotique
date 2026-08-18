import os
import subprocess
import sys
import signal
import time

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PYTHON_JAKA = os.path.join(BASE_DIR, "venv_jaka", "bin", "python")

SCRIPTS = ["ur5_telemetrie.py", "ur12e_telemetrie.py", "jaka_telemetrie.py"]

processes = []


def arreter_tous(signum=None, frame=None):
    print("\nArrêt de tous les scripts de télémétrie...")
    for name, p in processes:
        p.send_signal(signal.SIGINT)
    for name, p in processes:
        p.wait(timeout=10)
        print(f"[OK] {name} arrêté")
    sys.exit(0)


def main():
    signal.signal(signal.SIGINT, arreter_tous)
    signal.signal(signal.SIGTERM, arreter_tous)

    for script in SCRIPTS:
        if script == "jaka_telemetrie.py":
            python_bin = PYTHON_JAKA
        else:
            python_bin = sys.executable
        p = subprocess.Popen([python_bin, script], cwd=BASE_DIR)
        processes.append((script, p))
        print(f"[OK] {script} lancé (pid={p.pid}) avec {python_bin}")

    try:
        while True:
            for name, p in processes:
                if p.poll() is not None:
                    print(f"[AVERTISSEMENT] {name} s'est arrêté (code {p.returncode})")
            time.sleep(2)
    except KeyboardInterrupt:
        arreter_tous()


if __name__ == "__main__":
    main()
