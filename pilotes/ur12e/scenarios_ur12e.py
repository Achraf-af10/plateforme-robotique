"""
Scénarios métier UR12e (vissage, etc.)
Responsabilité : logique applicative, utilise l'API UR12e.
"""
import time
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "effecteurs"))
sys.path.insert(0, os.path.dirname(__file__))

from screwdriver import move_shank, tighten_screw, pick_screw
from grille_utils import (
    positions_grille, initialiser_grille,
    indice_courant_grille, consommer_element_grille,
)
from config_ur12e import (
    PLAN_DESSOUS, DEPART_P,
    SPEED_J, ACC_J, SPEED_L_FAST, ACC_L_FAST,
    SPEED_L_SLOW, ACC_L_SLOW,
    APPROACH_Z, Z_FORCE_N,
    TOL_OK, SLEEP_APRES, SPEED_SLIDER,
    POS_AVANT_DISTR_Q, POS_AVANT_DISTR_P,
    ATT_PRES_VIS_P, POS_RECUP_VIS_P,
    SPEED_L_PICKUP, ACC_L_PICKUP,
    CAPTEUR_PRES_VIS_PIN,
)


def _vers_base(robot, PLAN, point_platforme):
    """Transforme un point du repère plateforme vers le repère base robot."""
    return robot.pose_trans(PLAN, point_platforme)


def _aller_a(robot, pos_base):
    """MoveJ vers un point cartésien — IK depuis la position courante."""
    q = robot.get_inverse_kinematics(pos_base, qnear=robot.get_actual_q())
    robot.moveJ(q, SPEED_J, ACC_J)


def _prendre_vis(robot, vis):
    """Va au poste distributeur, attend la vis, et la prend avec la visseuse."""
    # Approche du distributeur
    robot.moveJ(POS_AVANT_DISTR_Q, SPEED_J, ACC_J)
    move_shank(z_pos_mm=20, tool_index=0)
    robot.moveL(ATT_PRES_VIS_P, SPEED_L_PICKUP, ACC_L_PICKUP)

    # Attente de la présence de la vis (capteur digital)
    print("  attente vis au distributeur...")
    while robot.get_digital_in(CAPTEUR_PRES_VIS_PIN) == False:
        time.sleep(0.01)

    # Descente sur la position de récupération
    robot.moveL(POS_RECUP_VIS_P, SPEED_L_PICKUP, ACC_L_PICKUP)

    # Prise de la vis
    retval = pick_screw(
        z_force_n=Z_FORCE_N,
        screw_length_mm=8.0,                                                                                    ######## A AJUSTER SELON LA VIS
        tool_index=0,
    )

    # Remontée, qu'il y ait échec ou succès
    robot.moveL(POS_AVANT_DISTR_P, SPEED_L_PICKUP, ACC_L_PICKUP)

    if retval != 0:
        print(f"  {vis['nom']} → echec prise de vis (code {retval})")
        return False

    print(f"  {vis['nom']} — vis prise")
    return True


def _visser_une_vis(robot, vis):
    pos_vis    = _vers_base(robot, vis["plan"], vis["pos_p"])
    rx, ry, rz = pos_vis[3], pos_vis[4], pos_vis[5]
    pos_avant  = [pos_vis[0], pos_vis[1], pos_vis[2] + APPROACH_Z, rx, ry, rz]

    # Prise de la vis au poste distributeur
    if not _prendre_vis(robot, vis):
        return False

    # Approche au-dessus de la vis
    q = robot.get_inverse_kinematics(pos_avant, qnear=robot.get_actual_q())
    robot.moveJ(q, SPEED_J, ACC_J)

    move_shank(z_pos_mm=vis["shank_mm"], tool_index=0)

    # Descente directe sur la vis
    robot.moveL(pos_vis, SPEED_L_SLOW, ACC_L_SLOW)

    # Vissage
    on_return, achieved, gradient = tighten_screw(
        z_force_n          = Z_FORCE_N,
        screwing_length_mm = vis["length"],
        torque_nm           = vis["torque_nm"],
        tool_index          = 0,
        timeout_ms          = 0.0,
    )

    print(f"  {vis['nom']} — couple = {achieved:.3f} Nm")

    # Remontée
    robot.moveL(pos_avant, SPEED_L_FAST, ACC_L_FAST)

    # Vérification couple
    if abs(achieved - vis["torque_nm"]) < TOL_OK:
        print(f"  {vis['nom']} → serree")
        if vis["sleep"]:
            move_shank(z_pos_mm=30, tool_index=0)
            time.sleep(SLEEP_APRES)
        return True

    print(f"  {vis['nom']} → NON serree")
    return False


def cycle_vissage(robot, vis_list):
    """Scénario principal : cycle de vissage de toutes les vis."""

    robot.set_speed_slider(SPEED_SLIDER)
    _aller_a(robot, DEPART_P)

    print("=== Début cycle de vissage ===")

    for vis in vis_list:
        print(f"\n--- {vis['nom']} ---")
        ok = _visser_une_vis(robot, vis)
        if not ok:
            print("\n=== Cycle interrompu ===")
            return False

    print("\n=== Cycle terminé — toutes les vis serrées ===")
    _aller_a(robot, DEPART_P)
    return True


# Vis disposees en grille (pas de poste distributeur, pas de capteur)
def _prendre_vis_grille(robot, vis, grille, indice):
    """
    Prend la vis d'indice `indice` dans la grille. Position deja connue
    (vis visible/disposee) : pas d'attente de capteur, descente directe.
    """
    positions = positions_grille(grille)
    if indice >= len(positions):
        raise RuntimeError(f"Grille epuisee ({grille['nom']})")

    pos_vis_p  = positions[indice]
    pos_vis    = robot.pose_trans(grille["plan"], pos_vis_p)
    rx, ry, rz = pos_vis[3], pos_vis[4], pos_vis[5]
    pos_avant  = [pos_vis[0], pos_vis[1], pos_vis[2] + APPROACH_Z, rx, ry, rz]

    # Approche au-dessus de la vis dans la grille
    q = robot.get_inverse_kinematics(pos_avant, qnear=robot.get_actual_q())
    robot.moveJ(q, SPEED_J, ACC_J)
    move_shank(z_pos_mm=30, tool_index=0) #########

    # Descente directe sur la vis
    robot.moveL(pos_vis, SPEED_L_SLOW, ACC_L_SLOW)

    # Prise de la vis
    retval = pick_screw(
        z_force_n=Z_FORCE_N,
        screw_length_mm=15.0, #########
        tool_index=0,
    )

    # Remontée
    robot.moveL(pos_avant, SPEED_L_FAST, ACC_L_FAST)

    if retval != 0:
        print(f"  {vis['nom']} → echec prise de vis en grille (code {retval})")
        return False

    consommer_element_grille(grille)
    print(f"  {vis['nom']} — vis prise (grille indice={indice})")
    return True


def _visser_une_vis_grille(robot, vis, grille, indice):
    """Meme sequence de vissage que _visser_une_vis, mais prise en grille."""
    pos_vis    = _vers_base(robot, vis["plan"], vis["pos_p"])
    rx, ry, rz = pos_vis[3], pos_vis[4], pos_vis[5]
    pos_avant  = [pos_vis[0], pos_vis[1], pos_vis[2] + APPROACH_Z, rx, ry, rz]

    if not _prendre_vis_grille(robot, vis, grille, indice):
        return False

    # Approche au-dessus de la vis a visser
    q = robot.get_inverse_kinematics(pos_avant, qnear=robot.get_actual_q())
    robot.moveJ(q, SPEED_J, ACC_J)

    move_shank(z_pos_mm=vis["shank_mm"], tool_index=0)

    # Descente directe sur la vis
    robot.moveL(pos_vis, SPEED_L_SLOW, ACC_L_SLOW)

    # Vissage
    on_return, achieved, gradient = tighten_screw(
        z_force_n          = Z_FORCE_N,
        screwing_length_mm = vis["length"],
        torque_nm           = vis["torque_nm"],
        tool_index          = 0,
        timeout_ms          = 0.0,
    )

    print(f"  {vis['nom']} — couple = {achieved:.3f} Nm")

    # Remontée
    robot.moveL(pos_avant, SPEED_L_FAST, ACC_L_FAST)

    # Vérification couple
    if abs(achieved - vis["torque_nm"]) < TOL_OK:
        print(f"  {vis['nom']} → serree")
        if vis["sleep"]:
            move_shank(z_pos_mm=30, tool_index=0)
            time.sleep(SLEEP_APRES)
        return True

    print(f"  {vis['nom']} → NON serree")
    return False


def cycle_vissage_grille(robot, vis_list, grille):
    """
    Scénario principal grille : visse toutes les vis de vis_list, chacune
    prise a l'indice courant de la grille (memorise dans grille['etat_file']).
    """
    robot.set_speed_slider(SPEED_SLIDER)
    _aller_a(robot, DEPART_P)

    print(f"=== Début cycle de vissage — {grille['nom']} ===")

    for vis in vis_list:
        indice = indice_courant_grille(grille)
        print(f"\n--- {vis['nom']} (grille indice {indice}) ---")
        try:
            ok = _visser_une_vis_grille(robot, vis, grille, indice)
        except RuntimeError as e:
            print(f"\n=== Cycle interrompu : {e} ===")
            return False
        if not ok:
            print("\n=== Cycle interrompu ===")
            return False

    print("\n=== Cycle terminé — toutes les vis serrées ===")
    _aller_a(robot, DEPART_P)
    return True