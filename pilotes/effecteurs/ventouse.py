from pymodbus.client import ModbusTcpClient
import time

# Identifiant Modbus du VGC10
SLAVE_ID = 65

# Registres de commande
REG_CTRL_A   = 0
REG_CTRL_B   = 1
REG_POWER    = 2
REG_VACUUM_A = 18
REG_VACUUM_B = 19

# États de la pince
IDLE    = 512
RELEASE = 0

# Connexion au VGC10
client = ModbusTcpClient("10.120.0.54", port=502)
client.connect()


def vgc10_grip(vac_a, vac_b, power_limit):
    # vac_a : niveau de vide du canal A
    # vac_b : niveau de vide du canal B
    # power_limit : limite de puissance

    # Prépare les commandes de vide
    cmd_a = 256 + vac_a
    cmd_b = 256 + vac_b

    # Définit la limite de puissance
    client.write_register(REG_POWER,  power_limit, device_id=SLAVE_ID)

    # Active le canal A
    client.write_register(REG_CTRL_A, cmd_a,        device_id=SLAVE_ID)

    # Active le canal B
    client.write_register(REG_CTRL_B, cmd_b,        device_id=SLAVE_ID)


def vgc10_release():
    # Désactive la puissance
    client.write_register(REG_POWER,  0,       device_id=SLAVE_ID)

    # Libère le canal A
    client.write_register(REG_CTRL_A, RELEASE, device_id=SLAVE_ID)

    # Libère le canal B
    client.write_register(REG_CTRL_B, RELEASE, device_id=SLAVE_ID)


# Références :
# https://www.robotbutikken.dk/wp-content/uploads/Onrobot_VG10_Vacuun_Gripper_User_Manual_V1.1.1_0.pdf
# Page 17-15