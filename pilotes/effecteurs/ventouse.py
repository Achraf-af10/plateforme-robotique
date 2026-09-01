from pymodbus.client import ModbusTcpClient
import time

SLAVE_ID = 65

REG_CTRL_A   = 0
REG_CTRL_B   = 1
REG_POWER    = 2
REG_VACUUM_A = 18
REG_VACUUM_B = 19

IDLE    = 512
RELEASE = 0

client = ModbusTcpClient("10.120.0.54", port=502)
client.connect()


def vgc10_grip(vac_a, vac_b, power_limit):
    cmd_a = 256 + vac_a
    cmd_b = 256 + vac_b
    client.write_register(REG_POWER,  power_limit, device_id=SLAVE_ID)
    client.write_register(REG_CTRL_A, cmd_a,        device_id=SLAVE_ID)
    client.write_register(REG_CTRL_B, cmd_b,        device_id=SLAVE_ID)


def vgc10_release():
    client.write_register(REG_POWER,  0,       device_id=SLAVE_ID)
    client.write_register(REG_CTRL_A, RELEASE, device_id=SLAVE_ID)
    client.write_register(REG_CTRL_B, RELEASE, device_id=SLAVE_ID)


# Références :
# https://www.robotbutikken.dk/wp-content/uploads/Onrobot_VG10_Vacuun_Gripper_User_Manual_V1.1.1_0.pdf
# Page 17-15