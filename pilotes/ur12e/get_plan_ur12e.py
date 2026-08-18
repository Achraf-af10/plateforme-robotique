# get_plan_ur12e.py
# Recupere Plane_platforme depuis le fichier .script UR et met a jour config_ur12e.py

import paramiko
import re
import os

ROBOT_IP   = "10.120.0.12"
ROBOT_USER = "root"
ROBOT_PASS = "ur12esafe"

# Fichier script qui contient le repere
SCRIPT_FILE = "/programs/achraff.script"

# Nom du repere dans le script
PLANE_NOM = "Plane_platforme"

# Fichier config local a mettre a jour
CONFIG_FILE = os.path.join(os.path.dirname(__file__), "config_ur12e.py")


def recuperer_script():
    """Recupere le fichier .script depuis le robot via SSH."""
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ROBOT_IP, username=ROBOT_USER, password=ROBOT_PASS, timeout=10)

    sftp = client.open_sftp()
    contenu = sftp.open(SCRIPT_FILE).read().decode("utf-8")
    sftp.close()
    client.close()

    return contenu


def extraire_plan(contenu):
    """
    Extrait les valeurs depuis la ligne :
    global Plane_platforme=p[x,y,z,rx,ry,rz]
    """
    pattern = rf'global\s+{re.escape(PLANE_NOM)}\s*=\s*p\[([^\]]+)\]'
    match = re.search(pattern, contenu)

    if not match:
        raise ValueError(f"'{PLANE_NOM}' non trouve dans {SCRIPT_FILE}")

    valeurs = [float(v.strip()) for v in match.group(1).split(",")]

    if len(valeurs) != 6:
        raise ValueError(f"Format invalide — attendu 6 valeurs, obtenu {len(valeurs)}")

    return valeurs


def mettre_a_jour_config(valeurs):
    """Remplace PLANE_PLATFORME dans config_ur12e.py."""
    with open(CONFIG_FILE, "r") as f:
        contenu = f.read()

    nouvelle_valeur = (
        f"PLANE_PLATFORME = [\n"
        f"    {valeurs[0]}, {valeurs[1]}, {valeurs[2]},\n"
        f"    {valeurs[3]}, {valeurs[4]}, {valeurs[5]}\n"
        f"]"
    )

    pattern = r"PLANE_PLATFORME\s*=\s*\[[^\]]+\]"
    nouveau_contenu = re.sub(pattern, nouvelle_valeur, contenu, flags=re.DOTALL)

    if nouveau_contenu == contenu:
        raise ValueError("PLANE_PLATFORME non trouve dans config_ur12e.py")

    with open(CONFIG_FILE, "w") as f:
        f.write(nouveau_contenu)


def main():
    print(f"Connexion au robot {ROBOT_IP}...")
    contenu = recuperer_script()
    print(f"Fichier recupere : {SCRIPT_FILE}")

    valeurs = extraire_plan(contenu)
    print(f"Repere trouve : {valeurs}")

    mettre_a_jour_config(valeurs)
    print("config_ur12e.py mis a jour")

    print(f"\nPLANE_PLATFORME = {valeurs}")


if __name__ == "__main__":
    main()