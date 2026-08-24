# get_plan_ur12e.py
# Recupere les plans depuis le fichier .script UR et met a jour config_ur12e.py

import paramiko
import re
import os

ROBOT_IP   = "10.120.0.12"
ROBOT_USER = "root"
ROBOT_PASS = "ur12esafe"

SCRIPT_FILE = "/programs/achraff.script"
CONFIG_FILE = os.path.join(os.path.dirname(__file__), "config_ur12e.py")


# Plans a recuperer : nom dans le script UR -> nom de la constante Python
PLANS = {
    "Plan_platforme"    : "PLAN_PLATFORME",
    "Plan_grille_vis"   : "PLAN_GRILLE_VIS",
}


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


def extraire_plans(contenu):
    """Extrait toutes les valeurs depuis les lignes global Plan_xxx=p[...]."""
    resultats = {}
    for nom_script, nom_config in PLANS.items():
        pattern = rf'global\s+{re.escape(nom_script)}\s*=\s*p\[([^\]]+)\]'
        match = re.search(pattern, contenu)
        if not match:
            print(f"  ATTENTION — '{nom_script}' non trouve dans le script")
            continue
        valeurs = [float(v.strip()) for v in match.group(1).split(",")]
        if len(valeurs) != 6:
            print(f"  ATTENTION — '{nom_script}' format invalide (6 valeurs attendues)")
            continue
        resultats[nom_config] = valeurs
        print(f"  {nom_config} = {valeurs}")
    return resultats


def mettre_a_jour_config(plans):
    """Remplace chaque bloc PLAN_xxx = [...] dans config_ur12e.py, sans toucher au reste."""
    with open(CONFIG_FILE, "r") as f:
        contenu = f.read()

    for nom_config, valeurs in plans.items():
        nouvelle_valeur = (
            f"{nom_config} = [\n"
            f"    {valeurs[0]}, {valeurs[1]}, {valeurs[2]},\n"
            f"    {valeurs[3]}, {valeurs[4]}, {valeurs[5]}\n"
            f"]"
        )

        pattern = rf"{nom_config}\s*=\s*\[[^\]]+\]"
        nouveau_contenu, nb_remplacements = re.subn(
            pattern, nouvelle_valeur, contenu, flags=re.DOTALL
        )

        if nb_remplacements == 0:
            print(f"  ATTENTION — '{nom_config}' non trouve dans config_ur12e.py (ignore)")
            continue

        contenu = nouveau_contenu

    with open(CONFIG_FILE, "w") as f:
        f.write(contenu)


def main():
    print(f"Connexion au UR12e {ROBOT_IP}...")
    contenu = recuperer_script()
    print(f"Fichier recupere : {SCRIPT_FILE}")

    print("\nExtraction des plans :")
    plans = extraire_plans(contenu)

    if not plans:
        print("Aucun plan trouve — arret")
        return

    mettre_a_jour_config(plans)

    print(f"\nconfig_ur12e.py mis a jour ({len(plans)} plans)")


if __name__ == "__main__":
    main()