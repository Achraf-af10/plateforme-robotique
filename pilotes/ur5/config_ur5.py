# config_ur5.py
# Fichier de configuration — modifier uniquement ce fichier

# Plans recuperes automatiquement depuis le UR5
# Ne pas modifier manuellement — utiliser get_plan_ur5.py

PLAN_L298N = [
    0.418238593679427, -0.07264063057785787, 0.054629031285512525,
    -0.009980600640348355, 0.013475422631230796, 0.0035962033968317767
]

PLAN_SUP_L298N = [
    0.25859946563812797, 0.10128196143332684, 0.055435528094722825,
    -0.001612208305453404, 0.0143345771339896, -0.0014386641824506348
]

PLAN_BRIDE = [
    0.2591475196833351, -0.32505596196590447, 0.056332707144241156,
    -0.005505655872565907, 0.016280692226465842, 0.007187635960520967
]

PLAN_RASPICO = [
    0.274542573182003, -0.08847211070617142, 0.05614104285744115,
    -0.010012930950814604, 0.01547814571460989, 0.0034606688352015517
]

PLAN_SUP1_RASPI = [
    0.44942511074809843, 0.11157921182130273, 0.0537866385327099,
    -0.007178263607420478, 0.026625257494291305, -0.0073050888947710025
]

PLAN_SUP2_RASPI = [
    0.5444312544260804, 0.11258247641381017, 0.05176595552374694,
    -0.005870813133568442, 0.006865554788143569, -0.016028547055720797
]

PLAN_SUP_PICO = [
    0.3546446401400102, 0.13131224931554597, 0.054551173955026816,
    0.01065775009190746, 0.018925480126909335, -0.006039246206596588
]

PLAN_PLATFORME = [
    0.20459706978239514, 0.529681927830157, 0.09814791481663673,
    -2.223279984894965, -2.2032471677717047, -0.0022877855287012864
]

# Position de depart
DEPART_Q = [
    2.3968450477696024e-05, -1.570796314870016, -1.57074481645693,
    -1.5707839171039026, 1.570831537246704, 5.992112710373476e-05
]

# Vitesses de mouvement
SPEED_J       = 0.3
ACC_J         = 0.3
SPEED_L_SLOW  = 0.05
ACC_L_SLOW    = 0.05
SPEED_L_RETRAIT = 0.1
ACC_L_RETRAIT   = 0.1

# Geometrie
EPAISSEUR_SUPPORT = 0.0115
MARGE_DETECTION   = 0.04

# Detection de contact
MARGE_FORCE      = 15.0  # N
TIMEOUT_CONTACT  = 8.0   # s

# Pince
PINCE_FORCE = 80
PINCE_SPEED = 100

# Declaration des supports
# plan_prise / plan_pose : reperes ou sont exprimes pt_prise / pt_pose
# pt_prise, pt_pose      : [x, y, z, rx, ry, rz] dans leur repere local
# ouverture_prise/pose   : ouverture de pince (mm) a la prise / a la pose
# etat_file              : fichier JSON de suivi de pile pour ce support

SUPPORT_PICO = {
    "nom"            : "Support Pico",
    "plan_prise"     : PLAN_SUP_PICO,
    "pt_prise"       : [0.03104, 0.06274, 0.03722, 2.333, -2.169, 0.087],
    "plan_pose"      : PLAN_PLATFORME,
    "pt_pose"        : [0.03, 0.01272, 0.00286, 0.031, 0.035, 1.513],
    "ouverture_prise": 40,
    "ouverture_pose" : 47,
    "etat_file"      : "etat_pile_support_pico.json",
}

SUPPORT_L298N = {
    "nom"            : "Support L298N",
    "plan_prise"     : PLAN_SUP_L298N,
    "pt_prise"       : [0.03193, 0.10632, 0.03824, 2.332, -2.178, 0.068],
    "plan_pose"      : PLAN_PLATFORME,
    "pt_pose"        : [0.02864, 0.08059, 0.00362, 0.008, -0.093, -3.194],
    "ouverture_prise": 71,
    "ouverture_pose" : 73,
    "etat_file"      : "etat_pile_support_l298n.json",
}


# Grille de pieces : position de depart, ecart, dimensions et centre a ignorer
# plan_prise / plan_pose : reperes pour la prise et la pose
# pts_pose : positions de pose des pieces
# ouverture_prise/pose : ouverture de la pince (mm)
# nb_par_cycle : nombre de pieces par cycle
# etat_file : fichier JSON pour sauvegarder l'avancement

BRIDE_MOTEUR = {
    "nom"            : "Bride moteur",
    "plan_prise"     : PLAN_BRIDE,          
    "pt_origine"     : [0.022,0.043,0.012,2.319,-2.181,0.022],
    "pas_x"          : 0.096,
    "pas_y"          : 0.087,
    "nb_lignes"      : 2,
    "nb_colonnes"    : 2,
    "sauter_centre"  : False,
    "plan_pose"      : PLAN_PLATFORME,
    "pts_pose"       : [
        [0.08895,0.15812,-0.01526,0.073,-0.004,-0.052],
        [0.08974,0.00585,-0.01295,0.0009,0.046,3.064], 
        
    ],
    "ouverture_prise": 50,
    "ouverture_pose" : 55, 
    "nb_par_cycle"   : 2,
    "etat_file"      : "etat_grille_bride_moteur.json",
}

CARTE_L298N = {
    "nom"            : "Carte L298N",
    "plan_prise"     : PLAN_L298N,        
    "pt_origine"     : [0.02, 0.05, 0.02, 2.333, -2.169, 0.087],
    "pas_x"          : 0.025,
    "pas_y"          : 0.025,
    "nb_lignes"      : 3,
    "nb_colonnes"    : 3,
    "sauter_centre"  : True,
    "plan_pose"      : PLAN_PLATFORME,
    "pts_pose"       : [
        [0.03, 0.01, 0.003, 0.031, 0.035, 1.513], #A AJUSTER
    ],
    "ouverture_prise": 40, #
    "ouverture_pose" : 47, #
    "nb_par_cycle"   : 1,
    "etat_file"      : "etat_grille_carte_l298n.json",
}