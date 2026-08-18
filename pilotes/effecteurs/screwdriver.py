# screwdriver.py
import xmlrpc.client
import time

proxy = xmlrpc.client.ServerProxy("http://10.120.0.52:41414/", allow_none=True)

def _wait_screwdriver():
    time.sleep(0.1)
    while proxy.sd_get_screwdriver_busy(0):
        time.sleep(0.05)

def _wait_shank():
    time.sleep(0.1)
    while proxy.sd_get_shank_busy(0):
        time.sleep(0.05)




def pick_screw(z_force_n, screw_length_mm, tool_index=0, timeout_ms=0.0):
    retval = proxy.sd_pickup_screw(tool_index, z_force_n, float(screw_length_mm))
    if retval < 0:
        return retval
    _wait_screwdriver()
    return proxy.sd_get_command_results(tool_index)

def tighten_screw(z_force_n, screwing_length_mm, torque_nm, tool_index=0, timeout_ms=0.0):
    retval = proxy.sd_tighten(tool_index, z_force_n, float(screwing_length_mm), float(torque_nm))
    if retval < 0:
        return retval, 0, 0
    _wait_screwdriver()
    achieved = proxy.sd_get_achieved_torque(tool_index)
    gradient = proxy.sd_get_torque_gradient(tool_index)
    retval   = proxy.sd_get_command_results(tool_index)
    return retval, achieved, gradient

def loosen_screw(z_force_n, unscrewing_length_mm, tool_index=0, timeout_ms=0.0):
    retval = proxy.sd_loosen(tool_index, z_force_n, float(unscrewing_length_mm))
    if retval < 0:
        return retval
    _wait_screwdriver()
    return proxy.sd_get_command_results(tool_index)

def move_shank(z_pos_mm, tool_index=0):
    retval = proxy.sd_move_shank(tool_index, z_pos_mm)
    if retval < 0:
        return retval
    _wait_shank()
    return proxy.sd_get_command_results(tool_index)