# get_plan_ur5.py
# Recupere les plans depuis le UR5 et met a jour config_ur5.py

import paramiko
import re
import os

ROBOT_IP   = "10.120.0.11"
ROBOT_USER = "root"
ROBOT_PASS = "easybot"

SCRIPT_FILE = "/programs/get_plan_ur5.script"
CONFIG_FILE = os.path.join(os.path.dirname(__file__), "config_ur5.py")

# Plans a recuperer
PLANS = [
    "Plan_L298N",
    "Plan_sup_L298N",
    "Plan_bride",
    "Plan_raspico",
    "Plan_sup1_raspi",
    "Plan_sup2_raspi",
    "Plan_sup_pico",
    "Plan_platforme",
]


def recuperer_script():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ROBOT_IP, username=ROBOT_USER, password=ROBOT_PASS, timeout=10)
    sftp = client.open_sftp()
    contenu = sftp.open(SCRIPT_FILE).read().decode("utf-8")
    sftp.close()
    client.close()
    return contenu


def extraire_plans(contenu):
    """Extrait toutes les valeurs depuis les lignes global Plan_xxx=p[...]"""
    resultats = {}
    for nom in PLANS:
        pattern = rf'global\s+{re.escape(nom)}\s*=\s*p\[([^\]]+)\]'
        match = re.search(pattern, contenu)
        if not match:
            print(f"  ATTENTION — '{nom}' non trouve dans le script")
            continue
        valeurs = [float(v.strip()) for v in match.group(1).split(",")]
        resultats[nom] = valeurs
        print(f"  {nom} = {valeurs}")
    return resultats


def generer_config(plans):
    """Genere le contenu de config_ur5.py avec tous les plans."""
    lignes = [
        "# config_ur5.py",
        "# Plans recuperes automatiquement depuis le UR5",
        "# Ne pas modifier manuellement — utiliser get_plan_ur5.py",
        "",
    ]
    for nom, valeurs in plans.items():
        lignes.append(f"{nom.upper()} = [")
        lignes.append(f"    {valeurs[0]}, {valeurs[1]}, {valeurs[2]},")
        lignes.append(f"    {valeurs[3]}, {valeurs[4]}, {valeurs[5]}")
        lignes.append(f"]")
        lignes.append("")
    return "\n".join(lignes)


def main():
    print(f"Connexion au UR5 {ROBOT_IP}...")
    contenu = recuperer_script()
    print(f"Fichier recupere : {SCRIPT_FILE}")

    print("\nExtraction des plans :")
    plans = extraire_plans(contenu)

    if not plans:
        print("Aucun plan trouve — arret")
        return

    contenu_config = generer_config(plans)

    with open(CONFIG_FILE, "w") as f:
        f.write(contenu_config)

    print(f"\nconfig_ur5.py genere avec {len(plans)} plans")


if __name__ == "__main__":
    main()