# config.py
# Fichier de configuration — modifier uniquement ce fichier

# IP du robot
ROBOT_IP = "10.120.0.12"

# Repere platforme
# Lire dans : Installation → Features → Plan_platforme
PLANE_PLATFORME = [
    -0.6101916853243428, -0.3251482171630037, 0.09725150958541628,
    1.2102472234599855, 1.204121164478851, 1.2003750805635027
]

# Position de depart du robot
DEPART_P = [-.468389945276, -.265797410841, .347327833617, 2.808481366023,  1.407848293600,  .000000000020]
DEPART_Q = [3.9333825026685885, -1.1515688858108355, -2.2034097993905704, -2.927281584613842,  -1.7076195776890835,  4.717135559628818]

# Vitesses de mouvement
SPEED_J      = 1.3962634015954636  # rad/s
ACC_J        = 1.0471975511965976  # rad/s²
SPEED_L_FAST = 1.2                 # m/s — deplacement rapide
ACC_L_FAST   = 0.25                # m/s²
SPEED_L_SLOW = 0.3                 # m/s — approche lente
ACC_L_SLOW   = 0.1                 # m/s²
APPROACH_Z   = 0.05                # m — hauteur approche au dessus du trou

# Parametres de vissage
Z_FORCE_N   = 20    # N  — force axiale poussee par le tournevis
TORQUE_NM   = 0.15   # Nm — couple cible
TOL_OK      = 0.04  # Nm — tolerance acceptable
TOL_NOK     = 0.01  # Nm — tolerance echec — arret du cycle
SLEEP_APRES = 4.0   # s  — attente distributeur apres vissage


# Vitesse globale du robot (0.0 a 1.0)
SPEED_SLIDER = 0.2

# Declaration des vis
# pos_p : [x(m), y(m), z(m), rx(rad), ry(rad), rz(rad)]
# shank_mm : position de la tige du tournevis en mm
# length   : longueur de vissage en mm
# sleep    : True = attendre le distributeur apres vissage

VIS = [
    {
        "nom"     : "Vis 1 L298N",
        "pos_p"   : [0.050, 0.013, -0.180, 1.442, -0.741, 0.747],
        "shank_mm": 40,
        "length"  : 3.0,
        "sleep"   : True,
    },
    {
        "nom"     : "Vis 2 L298N",
        "pos_p"   : [0.110, 0.013, -0.180, 1.442, -0.741, 0.747],
        "shank_mm": 40,
        "length"  : 3.0,
        "sleep"   : True,
    },
    {
        "nom"     : "Vis 3 L298N",
        "pos_p"   : [0.110, 0.013, -0.120, 1.442, -0.741, 0.747],
        "shank_mm": 40,
        "length"  : 3.0,
        "sleep"   : True,
    },
    {
        "nom"     : "Vis 4 L298N",
        "pos_p"   : [0.050, 0.013, -0.120, 1.442, -0.741, 0.747],
        "shank_mm": 40,
        "length"  : 3.0,
        "sleep"   : True,
    },
    {
        "nom"     : "Vis 5 RAP_PICO",
        "pos_p"   : [0.140, 0.013, -0.120, 1.442, -0.741, 0.747],
        "shank_mm": 40,
        "length"  : 3.0,
        "sleep"   : True,
    },
    {
        "nom"     : "Vis 6 RAP_PICO",
        "pos_p"   : [0.160, 0.013, -0.180, 1.442, -0.741, 0.747],
        "shank_mm": 40,
        "length"  : 3.0,
        "sleep"   : True,
    },
    {
        "nom"     : "Vis 7 RAP_PICO",
        "pos_p"   : [0.140, 0.013, -0.180, 1.442, -0.741, 0.747],
        "shank_mm": 40,
        "length"  : 3.0,
        "sleep"   : False,
    }
]