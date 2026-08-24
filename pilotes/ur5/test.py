# config.py
# Fichier de configuration — modifier uniquement ce fichier

# IP du robot
ROBOT_IP = "10.120.0.12"

# Repere platforme
# Lire dans : Installation → Features → Plan_platforme
PLAN_PLATFORME = [-0.6101916853243428, -0.3251482171630037, 0.09725150958541628,1.2102472234599855, 1.204121164478851, 1.2003750805635027]

PLAN_GRILLE_VIS = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

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
TOL_OK      = 0.07  # Nm — tolerance acceptable
TOL_NOK     = 0.01  # Nm — tolerance echec — arret du cycle
SLEEP_APRES = 4.0   # s  — attente distributeur apres vissage

# Poste de prise de vis (repère base robot)
POS_AVANT_DISTR_P = [-0.18383355653320946, -0.33031250000237367, 0.18779501033197865, 2.1649104235630365, 2.2721082803608876, 0.051894429792435366]
POS_AVANT_DISTR_Q = [4.5469818115234375, -0.9006555837443848, -2.592536449432373, -2.8100840053954066, -1.782729450856344, 4.738032817840576]
ATT_PRES_VIS_P    = [-0.183842896087681, -0.3303056674200616, 0.13038077702969672, 2.1649513017482933, 2.272104974595138, 0.05189791107895841]
POS_RECUP_VIS_P   = [-0.18383460381880662, -0.33032291856269497, 0.1068219865477667, 2.1648972497081194, 2.2721188342461427, 0.051841055658842304]


SPEED_L_PICKUP = 1.2
ACC_L_PICKUP   = 0.25

CAPTEUR_PRES_VIS_PIN = 0  # entrée digitale


# Vitesse globale du robot (0.0 a 1.0)
SPEED_SLIDER = 0.2

# Declaration des vis
# pos_p : [x(m), y(m), z(m), rx(rad), ry(rad), rz(rad)]
# shank_mm : position de la tige du tournevis en mm
# length   : longueur de vissage en mm
# "torque_nm": couple cible en Nm
# sleep    : True = attendre le distributeur apres vissage

VIS_SUP_PICO = [
    {
        "nom"     : "Vis 5 SUP_PICO",
        "pos_p"   : [0.140, 0.013, -0.120, 1.442, -0.741, 0.747],
        "shank_mm": 40,
        "length"  : 4.0,
        "torque_nm":0.15,
        "sleep"   : False,
    },
    {
        "nom"     : "Vis 6 SUP_PICO",
        "pos_p"   : [0.160, 0.013, -0.180, 1.442, -0.741, 0.747],
        "shank_mm": 40,
        "length"  : 4.0,
        "torque_nm":0.15,
        "sleep"   : False,
    },
    {
        "nom"     : "Vis 7 SUP_PICO",
        "pos_p"   : [0.140, 0.013, -0.180, 1.442, -0.741, 0.747],
        "shank_mm": 40,
        "length"  : 4.0,
        "torque_nm":0.15,
        "sleep"   : False,
    }
]

VIS_SUP_L298N = [
 {
        "nom"     : "Vis 1 SUP_L298N",
        "pos_p"   : [0.050, 0.013, -0.180, 1.442, -0.741, 0.747],
        "shank_mm": 40,
        "length"  : 4.0,
        "torque_nm":0.15,
        "sleep"   : False,
    },
    {
        "nom"     : "Vis 2 SUP_L298N",
        "pos_p"   : [0.110, 0.013, -0.180, 1.442, -0.741, 0.747],
        "shank_mm": 40,
        "length"  : 4.0,
        "torque_nm":0.15,
        "sleep"   : False,
    },
    {
        "nom"     : "Vis 3 SUP_L298N",
        "pos_p"   : [0.110, 0.013, -0.120, 1.442, -0.741, 0.747],
        "shank_mm": 40,
        "length"  : 4.0,
        "torque_nm":0.15,
        "sleep"   : False,
    },
    {
        "nom"     : "Vis 4 SUP_L298N",
        "pos_p"   : [0.050, 0.013, -0.120, 1.442, -0.741, 0.747],
        "shank_mm": 40,
        "length"  : 4.0,
        "torque_nm":0.15,
        "sleep"   : False,
    }
]

VIS_BRIDE_MOTEUR = [
 {
        "nom"     : "Vis 1 bride 1",
        "pos_p"   : [-0.0075, 0.013, -0.058, 1.442, -0.741, 0.747],
        "shank_mm": 40,
        "length"  : 2.0,
        "torque_nm":0.15,
        "sleep"   : False,
    },
    {
        "nom"     : "Vis 2 bride 1",
        "pos_p"   : [-0.0075, 0.013, -0.122, 1.442, -0.741, 0.747],
        "shank_mm": 40,
        "length"  : 2.0,
        "torque_nm":0.15,
        "sleep"   : False,
    },
    {
        "nom"     : "Vis 1 bride 2",
        "pos_p"   : [0.1675, 0.013, -0.058, 1.442, -0.741, 0.747],
        "shank_mm": 40,
        "length"  : 2.0,
        "torque_nm":0.15,
        "sleep"   : False,
    },
    {
        "nom"     : "Vis 2 bride 2",
        "pos_p"   : [0.1675, 0.013, -0.122, 1.442, -0.741, 0.747],
        "shank_mm": 40,
        "length"  : 2.0,
        "torque_nm":0.15,
        "sleep"   : False,
    }
]


# Grille de vis : positions, dimensions et centre a ignorer
# pt_origine : position de la premiere vis
# pas_x, pas_y : distance entre les vis (m)
# nb_lignes, nb_colonnes : taille de la grille
# sauter_centre : True pour ignorer le centre
# etat_file : fichier JSON pour sauvegarder l'avancement

GRILLE_VIS_8X8 = {
    "nom"          : "Grille vis 8x8",
    "plan"         : PLAN_GRILLE_VIS,
    "pt_origine"   : [0.0, 0.0, -0.008, 0.111,-3.138,0.067], 
    "pas_x"        : 0.010, 
    "pas_y"        : 0.010, 
    "nb_lignes"    : 8,
    "nb_colonnes"  : 8,
    "sauter_centre": False,
    "etat_file"    : "etat_grille_vis_8x8.json",
}