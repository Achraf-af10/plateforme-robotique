"""Tous les scénarios pour UR12e"""

def visser_support_pico(rtde_c, rtde_r, tighten_screw, data):
    """UR12e visse un support Pico"""
    print(f"[ur12e] Visser support Pico (N°{data.get('numero')})")
    
    # Point 1: approche
    point_approche = [-0.47, -0.26, 0.4, -2.88, -1.23, -0.07]
    rtde_c.moveL(point_approche, speed=0.1, acceleration=0.1)
    
    # Point 2: execution
    point_execution = [-0.47, -0.26, 0.15, -2.88, -1.23, -0.07]
    rtde_c.moveL(point_execution, speed=0.05, acceleration=0.05)
    
    # Paramètres du scénario
    z_force = data.get("z_force", 50)
    longueur = data.get("longueur", 20)
    couple = data.get("couple", 2.5)
    
    retval, achieved, gradient = tighten_screw(z_force_n=z_force, screwing_length_mm=longueur, torque_nm=couple)
    print(f"[ur12e] Vissage OK: torque={achieved}Nm")

def move_to_point_b(rtde_c, rtde_r, tighten_screw, data):
    """UR12e va au point B (demo)"""
    print("[ur12e] Move to point B")
    point_b = [-0.5072557911912113, -0.25443998332771245, 0.3574337933610186, -2.8795415568565432, -1.2341722001833153, -0.07000425237093798]
    rtde_c.moveL(point_b, speed=0.1, acceleration=0.1)

def move_to_point_e(rtde_c, rtde_r, tighten_screw, data):
    """UR12e va au point E (demo)"""
    print("[ur12e] Move to point E")
    point_e = [-0.6992066832523436, -0.2544319239003424, 0.3574493183361128, -2.879549786941135, -1.2341247557601733, -0.0699349585606065]
    rtde_c.moveL(point_e, speed=0.1, acceleration=0.1)

# Dictionnaire des scénarios disponibles
SCENARIOS = {
    "visser_support_pico": visser_support_pico,
    "move_to_point_b": move_to_point_b,
    "move_to_point_e": move_to_point_e,
}


# vissage.py
# Application principale — ne pas modifier sauf si tu changes la logique

from rtde_control import RTDEControlInterface
from rtde_receive import RTDEReceiveInterface
from rtde_io      import RTDEIOInterface
from config_ur12e       import (
    ROBOT_IP, PLANE_PLATFORME,
    SPEED_J, ACC_J,
)
import time
import math
import threading

# Connexion au robot
rtde_r = RTDEReceiveInterface(ROBOT_IP)
rtde_c = RTDEControlInterface(ROBOT_IP)
rtde_io = RTDEIOInterface(ROBOT_IP)





def _vers_base(point_platforme):
    # Transforme un point du repere platforme vers le repere base robot
    return rtde_c.poseTrans(PLANE_PLATFORME, point_platforme)


def _aller_a(pos_base):
    # MoveJ vers un point cartesien — IK depuis la position courante
    q = rtde_c.getInverseKinematics(pos_base, qnear=rtde_r.getActualQ())
    rtde_c.moveJ(q, SPEED_J, ACC_J)





