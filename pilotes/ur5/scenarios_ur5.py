import json
import os
import time

from effecteurs.pince_2FG7 import pince_close, pince_open
from ur5.config_ur5 import PLAN_SUP_PICO, PLAN_PLATFORME

# Paramètres de mouvement
SPEED_J, ACC_J = 0.3, 0.3
SPEED_L_FAST, ACC_L_FAST = 0.1, 0.1
SPEED_L_SLOW, ACC_L_SLOW = 0.05, 0.05

# Paramètres de la pile et détection
EPAISSEUR_SUPPORT = 0.0115
MARGE_DETECTION = 0.02
MARGE_FORCE = 8.0


# Fichier d'état persistant
ETAT_FILE = os.path.join(os.path.dirname(__file__), "etat_pile_support_l298n.json")

# Positions de départ et points fixes
depart_q = [2.3968450477696024e-05, -1.570796314870016, -1.57074481645693,-1.5707839171039026, 1.570831537246704, 5.992112710373476e-05]
pose  = [0.03, 0.01272, 0.00286, 0.031, 0.035, 1.513]
prise = [0.03104, 0.06274, 0.03722, 2.333, -2.169, 0.087]


#  --- Fonctions utilitaires ---
def _vers_base(rtde_c, point, plan):
    return rtde_c.poseTrans(plan, point)
 
 
def _aller_a(rtde_c, rtde_r, pos_base):
    q = rtde_c.getInverseKinematics(pos_base, qnear=rtde_r.getActualQ())
    rtde_c.moveJ(q, SPEED_J, ACC_J)
 
 
def _pos_avant(pos, delta_z):
    # pos = [x, y, z, rx, ry, rz] — decale Z de delta_z, ecrit explicitement
    return [pos[0], pos[1], pos[2] + delta_z, pos[3], pos[4], pos[5]]
 
 
# --- Gestion de l'état (JSON) ---
def _lire_etat():
    if not os.path.exists(ETAT_FILE): return {}
    with open(ETAT_FILE, "r") as f: return json.load(f)
 
 
def _ecrire_etat(etat):
    with open(ETAT_FILE, "w") as f: json.dump(etat, f)
 
 
def initialiser_pile_L298N(nb_support):
    _ecrire_etat({"nb_support": nb_support, "prochain_index": nb_support - 1})
    print(f"[ur5] Pile initialisée : {nb_support} supports")
 
 
def _index_courant():
    etat = _lire_etat()
    if "prochain_index" not in etat:
        raise RuntimeError("Pile non initialisée.")
    return etat["prochain_index"], etat["nb_support"]
 
 
def _consommer_support():
    etat = _lire_etat()
    etat["prochain_index"] -= 1
    _ecrire_etat(etat)
 
 
# --- Détection de contact (utilisee uniquement pour la PRISE) ---
def move_until_contact(rtde_c, rtde_r, xd, direction, marge_force=8.0,
                        nb_echantillons=10, delai_echantillon=0.01, timeout=8.0):
    """
    Descend jusqu'au contact.
    seuil = moyenne(residu) + max(marge_force, 3 * ecart_type(residu))
    """
    rtde_c.zeroFtSensor()
    time.sleep(0.5)
 
    # Echantillonnage du residu au repos (robot immobile, capteur tare)
    echantillons = []
    for _ in range(nb_echantillons):
        forces = rtde_r.getActualTCPForce()
        effort = sum(abs(forces[i]) * abs(direction[i]) for i in range(3))
        echantillons.append(effort)
        time.sleep(delai_echantillon)
 
    moyenne = sum(echantillons) / len(echantillons)
    variance = sum((e - moyenne) ** 2 for e in echantillons) / len(echantillons)
    ecart_type = variance ** 0.5
 
    seuil_force = moyenne + max(marge_force, 3 * ecart_type)
    print(f"  [debug] residu au repos: moyenne={moyenne:.2f} N, ecart-type={ecart_type:.2f} N")
    print(f"  [debug] seuil de contact calcule: {seuil_force:.2f} N")
    print(f"  [debug] xd={xd}")
    print(f"  [debug] TCP avant descente: {rtde_r.getActualTCPPose()}")
 
    rtde_c.speedL(xd, acceleration=ACC_L_SLOW, time=0.0)
 
    t0 = time.time()
    while (time.time() - t0) < timeout:
        forces = rtde_r.getActualTCPForce()
        effort = sum(abs(forces[i]) * abs(direction[i]) for i in range(3))
        if effort > seuil_force:
            rtde_c.speedStop(0.5)
            print(f"  [debug] contact detecte a t={time.time()-t0:.3f}s, effort={effort:.2f} N")
            print(f"  [debug] TCP au contact: {rtde_r.getActualTCPPose()}")
            return True
        time.sleep(0.01)
 
    rtde_c.speedStop(0.5)
    print(f"  [debug] TIMEOUT — TCP apres arret: {rtde_r.getActualTCPPose()}")
    return False
 
 
def _direction_descente(pt_haut, pt_bas):
    vect = [pt_bas[i] - pt_haut[i] for i in range(3)]
    norme = sum(c**2 for c in vect)**0.5
    dir_unit = [c / norme for c in vect]
    vitesse = [c * SPEED_L_SLOW for c in dir_unit] + [0, 0, 0]
    return vitesse, dir_unit + [0, 0, 0]
 
 
# --- Cycle principal ---
def prendre_support_L298N(rtde_c, rtde_r, data):
    index, nb_support = _index_courant()
    if index < 0: raise RuntimeError("Pile vide !")
 
    delta_z = index * EPAISSEUR_SUPPORT
 
    # Point de prise, decale selon la position dans la pile
    pos_prise = _pos_avant(prise, delta_z)
    pos_prise_avant = _pos_avant(pos_prise, MARGE_DETECTION)
 
    pt_approche = _vers_base(rtde_c, pos_prise_avant, PLAN_SUP_PICO)
    pt_prise    = _vers_base(rtde_c, pos_prise, PLAN_SUP_PICO)
 
    # Point de pose, fixe (via PLAN_PLATFORME) — deplacement direct, pas de detection de contact
    pos_pose_avant = _pos_avant(pose, -(MARGE_DETECTION + 0.05))
 
    pt_pose      = _vers_base(rtde_c, pose, PLAN_PLATFORME)
    pt_pose_app  = _vers_base(rtde_c, pos_pose_avant, PLAN_PLATFORME)
 
    # 1. Prise
    rtde_c.moveJ(depart_q, SPEED_J, ACC_J)
    pince_open(width=43, force=80, speed=100)
    _aller_a(rtde_c, rtde_r, pt_approche)
 
    v, d = _direction_descente(pt_approche, pt_prise)
    if not move_until_contact(rtde_c, rtde_r, v, d, MARGE_FORCE):
        raise RuntimeError("Échec contact prise.")

    
 
    pince_close(width=0.0, force=80, speed=100)

    _aller_a(rtde_c, rtde_r, pt_approche)
 
    # 2. Pose — moveL direct jusqu'au point de pose, sans detection de contact
    _aller_a(rtde_c, rtde_r, pt_pose_app)
    rtde_c.moveL(pt_pose, SPEED_L_SLOW, ACC_L_SLOW)
 
    pince_open(width=45, force=80, speed=100)
 
    # Remontee avant de retourner au depart
    rtde_c.moveL(pt_pose_app, SPEED_L_FAST, ACC_L_FAST)
 
    rtde_c.moveJ(depart_q, SPEED_J, ACC_J)
 
    _consommer_support()
 
