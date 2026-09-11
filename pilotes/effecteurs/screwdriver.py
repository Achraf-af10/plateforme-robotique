# screwdriver.py
import xmlrpc.client
import time

# Connexion au tournevis
proxy = xmlrpc.client.ServerProxy("http://10.120.0.52:41414/", allow_none=True)


def _wait_screwdriver():
    # Attend la fin du mouvement du tournevis
    time.sleep(0.1)
    while proxy.sd_get_screwdriver_busy(0):
        time.sleep(0.05)


def _wait_shank():
    # Attend la fin du mouvement de la tige
    time.sleep(0.1)
    while proxy.sd_get_shank_busy(0):
        time.sleep(0.05)


def pick_screw(z_force_n, screw_length_mm, tool_index=0, timeout_ms=0.0):
    # z_force_n : force d'appui en N
    # screw_length_mm : longueur de la vis en mm
    # tool_index : numéro de l'outil
    # timeout_ms : délai maximum en ms

    # Prend une vis
    retval = proxy.sd_pickup_screw(tool_index, z_force_n, float(screw_length_mm))
    if retval < 0:
        return retval

    # Attend la fin de l'opération
    _wait_screwdriver()
    return proxy.sd_get_command_results(tool_index)


def tighten_screw(z_force_n, screwing_length_mm, torque_nm, tool_index=0, timeout_ms=0.0):
    # z_force_n : force d'appui en N
    # screwing_length_mm : longueur de vissage en mm
    # torque_nm : couple de vissage en Nm
    # tool_index : numéro de l'outil
    # timeout_ms : délai maximum en ms

    # Visse la vis
    retval = proxy.sd_tighten(tool_index, z_force_n, float(screwing_length_mm), float(torque_nm))
    if retval < 0:
        return retval, 0, 0

    # Attend la fin du vissage
    _wait_screwdriver()

    # Récupère les résultats du vissage
    achieved = proxy.sd_get_achieved_torque(tool_index)
    gradient = proxy.sd_get_torque_gradient(tool_index)
    retval   = proxy.sd_get_command_results(tool_index)

    return retval, achieved, gradient


def loosen_screw(z_force_n, unscrewing_length_mm, tool_index=0, timeout_ms=0.0):
    # z_force_n : force d'appui en N
    # unscrewing_length_mm : longueur de dévissage en mm
    # tool_index : numéro de l'outil
    # timeout_ms : délai maximum en ms

    # Dévisse la vis
    retval = proxy.sd_loosen(tool_index, z_force_n, float(unscrewing_length_mm))
    if retval < 0:
        return retval

    # Attend la fin du dévissage
    _wait_screwdriver()
    return proxy.sd_get_command_results(tool_index)


def move_shank(z_pos_mm, tool_index=0):
    # z_pos_mm : position de la tige en mm
    # tool_index : numéro de l'outil

    # Déplace la tige
    retval = proxy.sd_move_shank(tool_index, z_pos_mm)
    if retval < 0:
        return retval

    # Attend la fin du mouvement
    _wait_shank()
    return proxy.sd_get_command_results(tool_index)