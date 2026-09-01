"""
Scénarios métier JAKA (pick-and-place, etc.)
Responsabilité : logique applicative.
"""
import time
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "effecteurs"))
sys.path.insert(0, os.path.dirname(__file__))

from ventouse import vgc10_grip, vgc10_release

# Paramètres de mouvement
ABS = 0
SPEED_J = 2.0      # rad/s
SPEED_L = 250.0    # mm/s

# Positions de départ
DEPART_Q = [5.3888774593357995, 1.0481649693212112, 1.8134082319959113, 1.8374565997501444, -1.5445592894011002, 3.9351751223217666]

# Point A (Prise)
POINT_A = {
    "approche_q": [5.464533815927767, 2.242800410432222, 0.9444081141197777, 1.4933295134058224, -1.6249854562244779, 4.241791593022088],
    "haut_p": [-429.73939, 633.33135, 332.85447, 3.0774308071326666, -0.006337290405888888, 2.794284302082333],
    "prise_p": [-429.73939, 633.33135, 272.85447, 3.0774308071326666, -0.006337290405888888, 2.794284302082333],
}

# Point B (Pose)
POINT_B = {
    "approche_q": [4.9598662862687, 2.419723561024278, 0.5918201953048889, 1.6744831674996223, -1.6260640696838111, 2.2094946419504002],
    "haut_p": [-90.89631, 824.93589, 338.73856, -3.0607814135502, 0.010517528426033334, -1.9339984384798334],
    "pose_p": [-90.89631, 824.93589, 273.73856, -3.0607814135502, 0.010517528426033334, -1.9339984384798334],
}


# Paramètres ventouse
GRIP_LEVEL = 20      # 0-15 (tu utilisais 20, je garde ta valeur)
GRIP_DELAY = 0.8     # s
RELEASE_DELAY = 6.0  # s
POWER_LIMIT = 500    # mW

def attendre(robot):
    """Attendre que le robot atteigne sa cible."""
    time.sleep(0.15)
    while True:
        ret = robot.is_in_pos()
        if ret[0] == 0 and ret[1]:
            break
        time.sleep(0.05)

def pick_and_place(robot):
    """Scénario principal : prendre une pièce en A et la poser en B."""
    print("=== Début transfert ===")

    try:
        # 1. Position initiale
        robot.joint_move(DEPART_Q, ABS, True, SPEED_J)
        attendre(robot)

        # 2. Approche POINT A
        robot.joint_move(POINT_A["approche_q"], ABS, True, SPEED_J)
        attendre(robot)

        # 3. Descente sur pièce
        robot.linear_move(POINT_A["prise_p"], ABS, False, SPEED_L)
        attendre(robot)

        # 4. Aspiration
        vgc10_grip(GRIP_LEVEL, GRIP_LEVEL, POWER_LIMIT)
        time.sleep(GRIP_DELAY)

        # 5. Remontée depuis POINT A
        robot.linear_move(POINT_A["haut_p"], ABS, False, SPEED_L)
        attendre(robot)

        # 6. Approche POINT B
        robot.joint_move(POINT_B["approche_q"], ABS, True, SPEED_J)
        attendre(robot)

        # 7. Descente et pose
        robot.linear_move(POINT_B["pose_p"], ABS, False, SPEED_L)
        attendre(robot)

        # Relâchement
        vgc10_release()
        time.sleep(RELEASE_DELAY)

        # Remontée finale
        robot.linear_move(POINT_B["haut_p"], ABS, False, SPEED_L)
        attendre(robot)

        # Retour au départ
        robot.joint_move(DEPART_Q, ABS, True, SPEED_J)
        attendre(robot)

        print("=== Transfert terminé avec succès ===")
        return True

    except Exception as e:
        print(f"[ERREUR] Transfert échoué : {e}")
        vgc10_release()
        return False