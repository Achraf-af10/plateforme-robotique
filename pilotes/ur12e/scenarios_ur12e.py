import time
import threading
import os
import time
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "effecteurs"))
sys.path.insert(0, os.path.dirname(__file__))  
from screwdriver import move_shank, tighten_screw

def afficher_force(rtde_r):
    # Thread de monitoring — affiche la force TCP toutes les secondes
    while True:
        try:
            fz = abs(rtde_r.getActualTCPForce()[2])
            # print(f"force: {fz:.2f} N")
        except Exception:
            pass
        time.sleep(1.0)


def _vers_base(rtde_c, plane_plateforme, point_platforme):
    # Transforme un point du repere platforme vers le repere base robot
    return rtde_c.poseTrans(plane_plateforme, point_platforme)


def _aller_a(rtde_c, rtde_r, pos_base, speed_j, acc_j):
    # MoveJ vers un point cartesien — IK depuis la position courante
    q = rtde_c.getInverseKinematics(pos_base, qnear=rtde_r.getActualQ())
    rtde_c.moveJ(q, speed_j, acc_j)


def _visser_une_vis(rtde_c, rtde_r, vis, config):
    pos_vis    = _vers_base(rtde_c, config.PLANE_PLATFORME, vis["pos_p"])
    rx, ry, rz = pos_vis[3], pos_vis[4], pos_vis[5]
    pos_avant  = [pos_vis[0], pos_vis[1], pos_vis[2] + config.APPROACH_Z, rx, ry, rz]

    # Approche au-dessus de la vis
    q = rtde_c.getInverseKinematics(pos_avant, qnear=rtde_r.getActualQ())
    rtde_c.moveJ(q, config.SPEED_J, config.ACC_J)

    # Descente directe sur la vis
    rtde_c.moveL(pos_vis, config.SPEED_L_SLOW, config.ACC_L_SLOW)

    # Vissage
    on_return, achieved, gradient = tighten_screw(
        z_force_n          = config.Z_FORCE_N,
        screwing_length_mm = vis["length"],
        torque_nm          = config.TORQUE_NM,
        tool_index         = 0,
        timeout_ms         = 0.0,
    )

    print(f"  {vis['nom']} — couple = {achieved:.3f} Nm")

    # Remontée
    rtde_c.moveL(pos_avant, config.SPEED_L_FAST, config.ACC_L_FAST)
    _aller_a(rtde_c, rtde_r, config.DEPART_P, config.SPEED_J, config.ACC_J)

    # Vérification couple
    if abs(achieved - config.TORQUE_NM) < config.TOL_OK:
        print(f"  {vis['nom']} → serree")
        if vis["sleep"]:
            move_shank(z_pos_mm=30, tool_index=0)
            time.sleep(config.SLEEP_APRES)
        return True

    print(f"  {vis['nom']} → NON serree")
    return False


def move(rtde_c, rtde_r, rtde_io, config):
    threading.Thread(target=afficher_force, args=(rtde_r,), daemon=True).start()
    rtde_io.setSpeedSlider(config.SPEED_SLIDER)

    move_shank(z_pos_mm=config.VIS[0]["shank_mm"], tool_index=0)
    _aller_a(rtde_c, rtde_r, config.DEPART_P, config.SPEED_J, config.ACC_J)

    print("=== Debut cycle de vissage ===")

    for vis in config.VIS:
        print(f"\n--- {vis['nom']} ---")
        move_shank(z_pos_mm=vis["shank_mm"], tool_index=0)
        ok = _visser_une_vis(rtde_c, rtde_r, vis, config)
        if not ok:
            print("\n=== Cycle interrompu ===")
            break
    else:
        print("\n=== Cycle termine — toutes les vis serrees ===")