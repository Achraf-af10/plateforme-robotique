"""
Scénarios métier UR5 — prendre et poser des pieces
"""
import json
import os
import time
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "effecteurs"))
sys.path.insert(0, os.path.dirname(__file__))

from pince_2FG7 import pince_close, pince_open
from grille_utils import (
    positions_grille, initialiser_grille,
    indice_courant_grille, consommer_element_grille,
)
from config_ur5 import (
    DEPART_Q,
    SPEED_J, ACC_J,
    SPEED_L_SLOW, ACC_L_SLOW,
    SPEED_L_RAPIDE, ACC_L_RAPIDE,
    SPEED_L_RETRAIT, ACC_L_RETRAIT,
    EPAISSEUR_SUPPORT, MARGE_DETECTION, MARGE_INTER,
    MARGE_FORCE, TIMEOUT_CONTACT,
    PINCE_FORCE, PINCE_SPEED
)


# Gestion de la pile (un fichier JSON par type de support)
def initialiser_pile(support, nb_support):
    with open(support["etat_file"], "w") as f:
        json.dump({"nb_support": nb_support, "prochain_index": nb_support - 1}, f)
    print(f"[scenarios] Pile initialisee ({support['nom']}) : {nb_support} supports")


def _index_courant(support):
    etat_file = support["etat_file"]
    
    # Si le fichier n'existe pas, on initialise la pile avec le nombre par défaut
    if not os.path.exists(etat_file):
        # On récupère 'nb_support' du dictionnaire (ex: support['nb_support'] ou une valeur par défaut)
        nb_support = support.get("nb_support", 5) 
        initialiser_pile(support, nb_support)

    with open(etat_file) as f:
        etat = json.load(f)

    # Sécurité si le fichier JSON est corrompu ou incomplet
    if "prochain_index" not in etat:
        nb_support = support.get("nb_support", 5)
        initialiser_pile(support, nb_support)
        with open(etat_file) as f:
            etat = json.load(f)

    return etat["prochain_index"], etat["nb_support"]


def _consommer_support(support):
    etat_file = support["etat_file"]
    with open(etat_file) as f:
        etat = json.load(f)
    etat["prochain_index"] -= 1
    with open(etat_file, "w") as f:
        json.dump(etat, f)


# Utilitaires
def _pos_avant(pos, delta_z):
    return [pos[0], pos[1], pos[2] + delta_z, pos[3], pos[4], pos[5]]


def _direction_descente(pt_haut, pt_bas):
    vect  = [pt_bas[i] - pt_haut[i] for i in range(3)]
    norme = sum(c**2 for c in vect) ** 0.5
    d     = [c / norme for c in vect] + [0, 0, 0]
    v     = [c * SPEED_L_SLOW for c in d[:3]] + [0, 0, 0]
    return v, d


def move_until_contact(robot, v, d, marge_force=MARGE_FORCE, timeout=TIMEOUT_CONTACT):
    """Descend en speedL jusqu'a detection de contact par force."""
    robot.zero_ft_sensor()
    time.sleep(0.5)

    # Mesure force de reference
    echantillons = []
    for _ in range(10):
        forces = robot.get_actual_force()
        echantillons.append(sum(abs(forces[i]) * abs(d[i]) for i in range(3)))
        time.sleep(0.01)
    moyenne    = sum(echantillons) / len(echantillons)
    ecart_type = (sum((e - moyenne) ** 2 for e in echantillons) / len(echantillons)) ** 0.5
    seuil      = moyenne + max(marge_force, 3 * ecart_type)
    print(f"  [contact] seuil={seuil:.2f} N")

    robot.speedL(v, acceleration=ACC_L_SLOW, time=0.0)
    t0 = time.time()

    while time.time() - t0 < timeout:
        forces = robot.get_actual_force()
        effort = sum(abs(forces[i]) * abs(d[i]) for i in range(3))
        if effort > seuil:
            robot.speedStop(0.5)
            print(f"  [contact] detecte a t={time.time()-t0:.3f}s")
            return True
        time.sleep(0.01)

    robot.speedStop(0.5)
    print("  [contact] TIMEOUT")
    return False

#############################################################################################################################
# Scenario generique prise + pose (une seule piece) des pieces dans un bac
#############################################################################################################################

def _prendre_et_poser_une_piece(robot, support):
    index, _ = _index_courant(support)
    if index < 0:
        raise RuntimeError(f"Pile vide ! ({support['nom']})")

    plan_prise      = support["plan_prise"]
    plan_pose       = support["plan_pose"]
    ouverture_prise = support["ouverture_prise"]
    fermeture_prise = support["fermeture_prise"]
    ouverture_pose  = support["ouverture_pose"]
    label           = support["nom"]

    delta_z         = index * EPAISSEUR_SUPPORT
    pos_prise       = _pos_avant(support["pt_prise"], delta_z)
    pos_prise_avant = _pos_avant(pos_prise, MARGE_DETECTION)
    pos_prise_inter = _pos_avant(pos_prise, MARGE_INTER)

    pt_approche = robot.pose_trans(plan_prise, pos_prise_avant)
    pt_inter    = robot.pose_trans(plan_prise, pos_prise_inter)
    pt_prise    = robot.pose_trans(plan_prise, pos_prise)

    pos_pose_avant = _pos_avant(support["pt_pose"], -(MARGE_DETECTION + 0.05))
    pt_pose        = robot.pose_trans(plan_pose, support["pt_pose"])
    pt_pose_app    = robot.pose_trans(plan_pose, pos_pose_avant)

    #######################################################################
    # Prise dans le bac
    #######################################################################

    robot.moveJ(DEPART_Q, SPEED_J, ACC_J) # aller au point de depart

    q = robot.get_inverse_kinematics(pt_approche, qnear=robot.get_actual_q()) # point actiqulaire
    robot.moveJ(q, SPEED_J, ACC_J) # aller au point d'approche
    pince_open(width=ouverture_prise, force=PINCE_FORCE, speed=PINCE_SPEED) # ouvre la pince

    # Segment 1 : approche -> inter (rapide)
    robot.moveL(pt_inter, SPEED_L_RAPIDE, ACC_L_RAPIDE) # aller au point intermedaire

    # Segment 2 : inter -> prise (lent, avec detection de contact)
    v, d = _direction_descente(pt_inter, pt_prise) # avancer jusqua detecter un contact
    if not move_until_contact(robot, v, d):
        raise RuntimeError(f"Echec contact {label}")

    pince_close(width=fermeture_prise, force=PINCE_FORCE, speed=PINCE_SPEED)

    robot.moveL(pt_approche, SPEED_L_RETRAIT, ACC_L_RETRAIT)

    #######################################################################
    # Pose dans la plateforme
    #######################################################################

    q = robot.get_inverse_kinematics(pt_pose_app, qnear=robot.get_actual_q())
    robot.moveJ(q, SPEED_J, ACC_J) # aller au point dapproche du point de pose
    robot.moveL(pt_pose, SPEED_L_SLOW, ACC_L_SLOW) # descend au point de pose

    pince_open(width=ouverture_pose, force=PINCE_FORCE, speed=PINCE_SPEED) # ouvre la pince pour lacher

    robot.moveL(pt_pose_app, SPEED_L_RETRAIT, ACC_L_RETRAIT) # aller au point dapproche
    robot.moveJ(DEPART_Q, SPEED_J, ACC_J) # aller au point de depart

    _consommer_support(support) # mise a jour des nombre de piece dans le bac
    print(f"[scenarios] {label} index={index} pose avec succes")

#######################################################################
# cycle des pieces dans un bac
#######################################################################
def cycle_pose(robot, support_list):
    """Scenario principal : pose successive de plusieurs pieces (memes ou types differents)."""
    print("=== Debut cycle de pose ===")

    for support in support_list:
        print(f"\n--- {support['nom']} ---")
        try:
            _prendre_et_poser_une_piece(robot, support)
        except RuntimeError as e:
            print(f"\n=== Cycle interrompu : {e} ===")
            return False

    print("\n=== Cycle termine — toutes les pieces posees ===")
    return True

#############################################################################################################################
# Pieces organisees en grille (pas de pile, positions calculees par pas x/y) les pieces dans une grille/matrice
#############################################################################################################################

def _prendre_et_poser_piece_grille(robot, grille, indice):
    """
    Prend la piece d'indice `indice` dans la grille et la pose au point
    pts_pose[indice] correspondant. Pas de move_until_contact : la hauteur
    de prise est connue (piece posee a plat, pas de pile).
    """
    positions = positions_grille(grille)
    pts_pose  = grille["pts_pose"]

    if indice >= len(positions):
        raise RuntimeError(f"Grille epuisee ({grille['nom']})")
    if indice >= len(pts_pose):
        raise RuntimeError(f"pts_pose insuffisant pour l'indice {indice} ({grille['nom']})")

    plan_prise      = grille["plan_prise"]
    plan_pose       = grille["plan_pose"]
    ouverture_prise = grille["ouverture_prise"]
    fermeture_prise = grille["fermeture_prise"]
    ouverture_pose  = grille["ouverture_pose"]
    label           = grille["nom"]

    pt_prise_local = positions[indice]
    pt_pose_local  = pts_pose[indice]

    pos_prise_avant = _pos_avant(pt_prise_local, MARGE_DETECTION)
    pos_prise_inter = _pos_avant(pt_prise_local, MARGE_INTER)
    pt_approche     = robot.pose_trans(plan_prise, pos_prise_avant)
    pt_inter        = robot.pose_trans(plan_prise, pos_prise_inter)
    pt_prise        = robot.pose_trans(plan_prise, pt_prise_local)

    pos_pose_avant = _pos_avant(pt_pose_local, -(MARGE_DETECTION + 0.05))
    pt_pose        = robot.pose_trans(plan_pose, pt_pose_local)
    pt_pose_app    = robot.pose_trans(plan_pose, pos_pose_avant)

    #######################################################################
    # Prise dans les grilles
    #######################################################################
    robot.moveJ(DEPART_Q, SPEED_J, ACC_J)

    q = robot.get_inverse_kinematics(pt_approche, qnear=robot.get_actual_q())
    robot.moveJ(q, SPEED_J, ACC_J)
    pince_open(width=ouverture_prise, force=PINCE_FORCE, speed=PINCE_SPEED)

    # Segment 1 : approche -> inter (rapide)
    robot.moveL(pt_inter, SPEED_L_RAPIDE, ACC_L_RAPIDE)

    # Segment 2 : inter -> prise (lent)
    robot.moveL(pt_prise, SPEED_L_SLOW, ACC_L_SLOW)

    pince_close(width=fermeture_prise, force=PINCE_FORCE, speed=PINCE_SPEED)

    robot.moveL(pt_approche, SPEED_L_RETRAIT, ACC_L_RETRAIT)

    #######################################################################
    # pose sur la plateforme
    #######################################################################
    q = robot.get_inverse_kinematics(pt_pose_app, qnear=robot.get_actual_q())
    robot.moveJ(q, SPEED_J, ACC_J)
    robot.moveL(pt_pose, SPEED_L_SLOW, ACC_L_SLOW)

    pince_open(width=ouverture_pose, force=PINCE_FORCE, speed=PINCE_SPEED)

    robot.moveL(pt_pose_app, SPEED_L_RETRAIT, ACC_L_RETRAIT)
    robot.moveJ(DEPART_Q, SPEED_J, ACC_J)

    consommer_element_grille(grille)
    print(f"[scenarios] {label} indice={indice} pose avec succes")

#######################################################################
# cycle des pieces dans une grilles
#######################################################################
def cycle_pose_grille(robot, grille):
    """
    Scenario principal grille : prend et pose grille['nb_par_cycle'] pieces
    a partir de l'indice courant, memorise entre deux appels via etat_file.
    """
    print(f"=== Debut cycle de pose — {grille['nom']} ===")

    for _ in range(grille["nb_par_cycle"]):
        indice = indice_courant_grille(grille)
        print(f"\n--- {grille['nom']} indice {indice} ---")
        try:
            _prendre_et_poser_piece_grille(robot, grille, indice)
        except RuntimeError as e:
            print(f"\n=== Cycle interrompu : {e} ===")
            return False

    print(f"\n=== Cycle termine — {grille['nom']} ===")
    return True