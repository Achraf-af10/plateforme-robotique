# config.py
# Fichier de configuration — modifier uniquement ce fichier

# IP du robot
ROBOT_IP = "10.120.0.12"

# Repere platforme
# Lire dans : Installation → Features → Plan_dessous

# repere plateforme de travail (dessous)
PLAN_DESSOUS = [
    -0.5970260916850079, -0.17030350362133234, 0.1378430066594293,
    -0.025410328826241283, -3.1186158149200596, -0.0002425257151249174
]
# repere plateforme de travail (dessus)
PLAN_DESSUS = [
    -0.5929315104498629, 0.11775699369668326, 0.13595769370944163,
    -0.013090051889887456, -3.1244074003359943, -0.0039059555192904618
]

# repere grille vis
PLAN_GRILLE_VIS = [
    -0.8959161713090482, 0.23576517757556736, 0.06596752920688348,
    0.001081517660900019, -0.0004957462252589081, 3.141363497313716
]

#repere grille entretoise
PLAN_GRILLE_ENTRETOISE = [
    -0.8972415661796301, 0.1560410116680353, 0.0600358198893394,
    0.0013067249844254877, -0.001012514419109025, -3.1283547476391584
]

"""
PLAN_GABARIT=[0, 0, 0, 0, 0, 0]
"""

# Position de depart du robot
DEPART_P = [-0.3956864294453475, 0.17756706448267412, 0.40527805128328587, -3.1346503212880057, 0.020412230169718736, 0.05712481823912654]
DEPART_Q = [3.150883197784424, -0.8645792764476319, -2.237497568130493, -3.1444417438902796, -1.5488246122943323, 4.710142612457275]

##########################################
# visseuse : parametres de vissage
##########################################

# Vitesses de mouvement
SPEED_J      = 0.349066              # rad/s
ACC_J        = 0.261799              # rad/s²
SPEED_L_FAST = 0.8                   # m/s — deplacement rapide
ACC_L_FAST   = 0.3                   # m/s²
SPEED_L_SLOW = 0.02                  # m/s — approche lente
ACC_L_SLOW   = 0.015                 # m/s²
APPROACH_Z   = 0.05                  # m — hauteur approche au dessus du trou
SPEED_L_PICKUP = 0.2
ACC_L_PICKUP   = 0.15



# Parametres de vissage
Z_FORCE_N   = 20    # N  — force axiale poussee par le tournevis
TOL_OK      = 0.1   # Nm — tolerance acceptable
TOL_NOK     = 0.01  # Nm — tolerance echec — arret du cycle
SLEEP_APRES = 4.0   # s  — attente distributeur apres vissage

# Poste de prise de vis (repère base robot)
POS_AVANT_DISTR_P = [-0.18383355653320946, -0.33031250000237367, 0.18779501033197865, 2.1649104235630365, 2.2721082803608876, 0.051894429792435366]
POS_AVANT_DISTR_Q = [4.5469818115234375, -0.9006555837443848, -2.592536449432373, -2.8100840053954066, -1.782729450856344, 4.738032817840576]
ATT_PRES_VIS_P    = [-0.183842896087681, -0.3303056674200616, 0.13038077702969672, 2.1649513017482933, 2.272104974595138, 0.05189791107895841]
POS_RECUP_VIS_P   = [-0.18383460381880662, -0.33032291856269497, 0.1068219865477667, 2.1648972497081194, 2.2721188342461427, 0.051841055658842304]




CAPTEUR_PRES_VIS_PIN = 0  # entrée digitale


# Vitesse globale du robot (0.0 a 1.0)
SPEED_SLIDER = 0.7

import os

# Remonte d'un niveau pour cibler 'pilotes/etats'
DOSSIER_ETATS = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "etats_json"))
os.makedirs(DOSSIER_ETATS, exist_ok=True)

# Declaration des vis
#plan : repere ou est exprime pos_p
# pos_p : [x(m), y(m), z(m), rx(rad), ry(rad), rz(rad)]
# shank_mm : position de la tige du tournevis en mm
# length   : longueur de vissage en mm
# torque_nm: couple cible en Nm
# sleep    : True = attendre le distributeur apres vissage

################################################################
# declarer les point ou on vis
################################################################


"""
VIS_SUP_PICO = [
    {
        "nom"     : "Vis 5 SUP_PICO",
        "plan"    : PLAN_DESSOUS,# repere 
        "pos_p"   : [0.020, 0.120, -0.0070, 0 ,0 ,3.016], # point de vissage du vis 1 dans le repere de la plateforme en dessous
        "shank_mm": 40, # la sortie de la tige avant d'arriver point de vissage
        "length"  : 4.0, # longeur de vissage du vis
        "torque_nm":0.15, # couple de vissage
        "sleep"   : False, # false pour ne attendre un temp avant de prendre le vis
    },
    {
        "nom"     : "Vis 7 SUP_PICO",
        "plan"    : PLAN_DESSOUS,
        "pos_p"   : [0.0, 0.180, -0.0070, 0 ,0 ,3.016],
        "shank_mm": 40,
        "length"  : 4.0,
        "torque_nm":0.15,
        "sleep"   : False,
    }
]
"""

VIS_SUP_PICO = [
    {
        "nom"     : "Vis 5 SUP_PICO",
        "plan"    : PLAN_DESSOUS,
        "pos_p"   : [0.020, 0.120, -0.0070, 0 ,0 ,3.016],
        "shank_mm": 40,
        "length"  : 4.0,
        "torque_nm":0.15,
        "sleep"   : False,
    },
    {
        "nom"     : "Vis 7 SUP_PICO",
        "plan"    : PLAN_DESSOUS,
        "pos_p"   : [0.0, 0.180, -0.0070, 0 ,0 ,3.016],
        "shank_mm": 40,
        "length"  : 4.0,
        "torque_nm":0.15,
        "sleep"   : False,
    }
]

VIS_SUP_L298N = [
 {
        "nom"     : "Vis 1 SUP_L298N",
        "plan"    : PLAN_DESSOUS,
        "pos_p"   : [0.050, 0.120, -0.0070, 0 ,0 ,3.016],
        "shank_mm": 40,
        "length"  : 4.0,
        "torque_nm":0.15,
        "sleep"   : False,
    },
    {
        "nom"     : "Vis 4 SUP_L298N",
        "plan"    : PLAN_DESSOUS,
        "pos_p"   : [0.110, 0.180, -0.0070, 0 ,0 ,3.016],
        "shank_mm": 40,
        "length"  : 4.0,
        "torque_nm":0.15,
        "sleep"   : False,
    }
]

VIS_BRIDE_MOTEUR = [

    {
        "nom"     : "Vis 2 bride 1",
        "plan"    : PLAN_DESSOUS,
        "pos_p"   : [-0.0075, 0.0580, -0.0010, 0,0,3.016],
        "shank_mm": 35,
        "length"  : 10.0,
        "torque_nm":0.2,
        "sleep"   : False,
    },
    {
        "nom"     : "Vis 2 bride 2",
        "plan"    : PLAN_DESSOUS,
        "pos_p"   : [0.1675, 0.0580, -0.0010, 0, 0, 3.016],
        "shank_mm": 35,
        "length"  : 10.0,
        "torque_nm":0.2,
        "sleep"   : False,
    }
]

VIS_SUP1_RASPI= [
 {
        "nom"     : "Vis 1 SUP1_RASPI",
        "plan"    : PLAN_DESSUS,
        "pos_p"   : [0.110, 0.140, -0.0080, 0 ,0 ,3.039],
        "shank_mm": 40,
        "length"  : 4.0,
        "torque_nm":0.15,
        "sleep"   : False,
    },
    {
        "nom"     : "Vis 4 SUP1_RASPI",
        "plan"    : PLAN_DESSUS,
        "pos_p"   : [0.150, 0.180, -0.0080, 0 ,0 ,3.039],
        "shank_mm": 40,
        "length"  : 4.0,
        "torque_nm":0.15,
        "sleep"   : False,
    }
]

VIS_SUP2_RASPI= [
 {
        "nom"     : "Vis 1 SUP2_RASPI",
        "plan"    : PLAN_DESSUS,
        "pos_p"   : [0.130, 0.125, -0.010, 0 ,0 ,3.151],
        "shank_mm": 40,
        "length"  : 2.0,
        "torque_nm":0.15,
        "sleep"   : False,
    }
]

VIS_ENTRETOISE_SUP_PICO = [
 {
        "nom"     : "Entretoise 1 SUP_PICO",
        "plan"    : PLAN_DESSOUS,
        "pos_p"   : [0.020, 0.120, 0.001, 0.033, 0.028, -4.025],
        "shank_mm": 20,
        "length"  : 7.0,
        "torque_nm":0.2,
        "sleep"   : False,
    },
    {
        "nom"     : "Entretoise 2 SUP_PICO",
        "plan"    : PLAN_DESSOUS,
        "pos_p"   : [0.020, 0.180, 0.001, 0.033, 0.028, -4.025],
        "shank_mm": 20,
        "length"  : 7.0,
        "torque_nm":0.2,
        "sleep"   : False,
    },
    {
        "nom"     : "Entretoise 3 SUP_PICO",
        "plan"    : PLAN_DESSOUS,
        "pos_p"   : [0.0, 0.180, 0.001, 0.033, 0.028, -4.025],
        "shank_mm": 20,
        "length"  : 7.0,
        "torque_nm":0.2,
        "sleep"   : False,
    }
]

VIS_ENTRETOISE_SUP_L298N = [
 {
        "nom"     : "Entretoise 1 SUP_L298N",
        "plan"    : PLAN_DESSOUS,
        "pos_p"   : [0.050, 0.120, 0.001, 0.033, 0.028, -4.025],
        "shank_mm": 20,
        "length"  : 7.0,
        "torque_nm":0.2,
        "sleep"   : False,
    },
    {
        "nom"     : "Entretoise 2 SUP_L298N",
        "plan"    : PLAN_DESSOUS,
        "pos_p"   : [0.050, 0.180, 0.001, 0.033, 0.028, -4.025],
        "shank_mm": 20,
        "length"  : 7.0,
        "torque_nm":0.2,
        "sleep"   : False,
    },
    {
        "nom"     : "Entretoise 3 SUP_L298N",
        "plan"    : PLAN_DESSOUS,
        "pos_p"   : [0.110, 0.120, 0.001, 0.033, 0.028, -4.025],
        "shank_mm": 20,
        "length"  : 7.0,
        "torque_nm":0.2,
        "sleep"   : False,
    },
    {
        "nom"     : "Entretoise 4 SUP_L298N",
        "plan"    : PLAN_DESSOUS,
        "pos_p"   : [0.110, 0.180, 0.001, 0.033, 0.028, -4.025],
        "shank_mm": 20,
        "length"  : 7.0,
        "torque_nm":0.2,
        "sleep"   : False,
    }
]

VIS_ENTRETOISE_SUP1_RASPI= [
 {
        "nom"     : "Entretoise 1 SUP_RASPI",
        "plan"    : PLAN_DESSUS,
        "pos_p"   : [0.110, 0.140, -0.0020, 0.064, -0.004, -3.488],
        "shank_mm": 20,
        "length"  : 7.0,
        "torque_nm":0.2,
        "sleep"   : False,
    },
    {
        "nom"     : "Entretoise 2 SUP_RASPI",
        "plan"    : PLAN_DESSUS,
        "pos_p"   : [0.110, 0.180, -0.0020, 0.064, -0.004, -3.488],
        "shank_mm": 20,
        "length"  : 7.0,
        "torque_nm":0.2,
        "sleep"   : False,
    },
    {
        "nom"     : "Entretoise 3 SUP_RASPI",
        "plan"    : PLAN_DESSUS,
        "pos_p"   : [0.150, 0.140, -0.0020, 0.064, -0.004, -3.488],
        "shank_mm": 20,
        "length"  : 7.0,
        "torque_nm":0.2,
        "sleep"   : False,
    },
    {
        "nom"     : "Entretoise 4 SUP_RASPI",
        "plan"    : PLAN_DESSUS,
        "pos_p"   : [0.150, 0.180, -0.0020, 0.064, -0.004, -3.488],
        "shank_mm": 20,
        "length"  : 7.0,
        "torque_nm":0.2,
        "sleep"   : False,
    }
]


VIS_SUP_POWERBANK = [

    {
        "nom"     : "Vis 1 sup_powerbank",
        "plan"    : PLAN_DESSUS,
        "pos_p"   : [0.060, 0.140, 0.001, 0.055, -0.014, -3.132],
        "shank_mm": 30,
        "length"  : 10.0,
        "torque_nm":0.2,
        "sleep"   : False,
    },
    {
        "nom"     : "Vis 2 sup_powerbank",
        "plan"    : PLAN_DESSUS,
        "pos_p"   : [0.020, 0.140, 0.001, 0.055, -0.014, -3.132],
        "shank_mm": 30,
        "length"  : 10.0,
        "torque_nm":0.2,
        "sleep"   : False,
    }
]


# Grille de vis : positions, dimensions et centre a ignorer
# pt_origine : position de la premiere vis
# pas_x, pas_y : distance entre les vis (m)
# nb_lignes, nb_colonnes : taille de la grille
# sauter_centre : True pour ignorer le centre
# etat_file : fichier JSON pour sauvegarder l'avancement

################################################################
# declarer les point ou on prendre les vis et entretoise
################################################################

"""
GRILLE_VIS_8X8 = {
    "nom"          : "Grille vis 8x8",
    "plan"         : PLAN_GRILLE_VIS, # repere de la grille des vis
    "pt_origine"   : [0.0, 0.0, -0.008, 0.02, 3.142, 0.0], # premier point du 1er vis
    "shank_mm"     : 30, # position de la tige du tournevis avant de prendre le vis
    "scew_length"  : 15.0, # langeur du vis
    "pas_x"        : 0.010, # # l'incrementation sur laxe x
    "pas_y"        : 0.010, # l'incrementation sur laxe y
    "nb_lignes"    : 8, # nombre de vis dans la matrice ligne
    "nb_colonnes"  : 8, # nombre de vis dans la matrice colonne
    "sauter_centre": False, # false : pour ne pas sauter le centre de la grille et true : pour sauter le centre
    "etat_file"    : os.path.join(DOSSIER_ETATS, "etat_grille_vis_8x8.json"),
}
"""

GRILLE_VIS_8X8 = {
    "nom"          : "Grille vis 8x8",
    "plan"         : PLAN_GRILLE_VIS,
    "pt_origine"   : [0.0, 0.0, -0.008, 0.02, 3.142, 0.0],
    "shank_mm"     : 30,
    "scew_length"  : 15.0,
    "pas_x"        : 0.010, 
    "pas_y"        : 0.010, 
    "nb_lignes"    : 8,
    "nb_colonnes"  : 8,
    "sauter_centre": False,
    "etat_file"    : os.path.join(DOSSIER_ETATS, "etat_grille_vis_8x8.json"),
}

GRILLE_ENTRETOISE_8X8 = {
    "nom"          : "Grille entretoise 8x8",
    "plan"         : PLAN_GRILLE_ENTRETOISE,
    "pt_origine"   : [0.0, 0.0, -0.001, 0.516, -3.100, 0.001],
    "shank_mm"     : 10,
    "scew_length"  : 3.0,
    "pas_x"        : 0.010,
    "pas_y"        : 0.010, 
    "nb_lignes"    : 8,
    "nb_colonnes"  : 8,
    "sauter_centre": False,
    "etat_file"    : os.path.join(DOSSIER_ETATS, "etat_grille_entretoise_8x8.json"),
}