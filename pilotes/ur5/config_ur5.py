# config_ur5.py
# Fichier de configuration — modifier uniquement ce fichier

# Plans recuperes automatiquement depuis le UR5
# Ne pas modifier manuellement — utiliser get_plan_ur5.py

PLAN_L298N = [
    0.418238593679427, -0.07264063057785787, 0.054629031285512525,
    -0.009980600640348355, 0.013475422631230796, 0.0035962033968317767
]

PLAN_SUP_L298N = [
    0.2583355832413213, 0.1008712811402028, 0.05526682991115017,
    -0.0029044534828139173, 0.00986015656214554, -0.003402793806365101
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
    0.354603597794066, 0.1305679601685348, 0.05432480830105285,
    -0.0006821406628018361, 0.006154342201653752, 0.00031274255227912843
]

PLAN_PLATFORME = [
    0.20686682304554002, 0.5271760788594813, 0.0989559426911131,
    -2.212125927979211, -2.222899956105486, -0.006495108118432681
]

# Position de depart
DEPART_Q = [
    2.3968450477696024e-05, -1.570796314870016, -1.57074481645693,
    -1.5707839171039026, 1.570831537246704, 5.992112710373476e-05
]

# Vitesses de mouvement
SPEED_J       = 0.5
ACC_J         = 0.8
SPEED_L_SLOW  = 0.02
ACC_L_SLOW    = 0.04
SPEED_L_RETRAIT = 0.15
ACC_L_RETRAIT   = 0.15

# Geometrie & Piles
EPAISSEUR_SUPPORT  = 0.0115
MARGE_DETECTION    = 0.04
NBR_SUPPORT_PICO   = 5
NBR_SUPPORT_L298N  = 5

# Detection de contact
MARGE_FORCE      = 15.0  # N
TIMEOUT_CONTACT  = 20.0   # s

# Pince
PINCE_FORCE = 80
PINCE_SPEED = 100

SPEED_SLIDER = 0.9

# Declaration des supports
# plan_prise / plan_pose : reperes ou sont exprimes pt_prise / pt_pose
# pt_prise, pt_pose      : [x, y, z, rx, ry, rz] dans leur repere local
# ouverture_prise/pose   : ouverture de pince (mm) a la prise / a la pose
# etat_file              : fichier JSON de suivi de pile pour ce support
# nb_support             : nombre initial de pieces dans la pile

import os

# Remonte d'un niveau pour cibler 'pilotes/etats'
DOSSIER_ETATS = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "etats_json"))
os.makedirs(DOSSIER_ETATS, exist_ok=True)

SUPPORT_PICO = {
    "nom"            : "Support Pico",
    "plan_prise"     : PLAN_SUP_PICO,
    "pt_prise"       : [0.03104, 0.06274, 0.03722, 2.333, -2.169, 0.087],
    "plan_pose"      : PLAN_PLATFORME,
    "pt_pose"        : [0.02992, 0.01227,0.0045,0.018,0.012,1.513],
    "ouverture_prise": 40,
    "ouverture_pose" : 47,
    "etat_file"      : os.path.join(DOSSIER_ETATS, "etat_pile_support_pico.json"),
    "nb_support"     : NBR_SUPPORT_PICO,
}

SUPPORT_L298N = {
    "nom"            : "Support L298N",
    "plan_prise"     : PLAN_SUP_L298N,
    "pt_prise"       : [0.03193, 0.10632, 0.03824, 2.332, -2.178, 0.068],
    "plan_pose"      : PLAN_PLATFORME,
    "pt_pose"        : [0.02850, 0.08160, 0.00455, 0.008, -0.1, -3.194],
    "ouverture_prise": 70,
    "ouverture_pose" : 73,
    "etat_file"      : os.path.join(DOSSIER_ETATS, "etat_pile_support_l298n.json"),
    "nb_support"     : NBR_SUPPORT_L298N,
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
        [0.08933,0.15818,-0.01076,0.073,-0.004,-0.052],
        [0.08810,0.00597,-0.00833,0.009,0.046,3.064], 
    ],
    "ouverture_prise": 50,
    "ouverture_pose" : 55, 
    "nb_par_cycle"   : 2,
    "etat_file"      : os.path.join(DOSSIER_ETATS, "etat_grille_bride_moteur.json"),
}

CARTE_L298N = {
    "nom"            : "Carte L298N",
    "plan_prise"     : PLAN_L298N,        
    "pt_origine"     : [0.0, 0.0, 0.02, 2.333, -2.169, 0.087],
    "pas_x"          : 0.025,
    "pas_y"          : 0.025,
    "nb_lignes"      : 3,
    "nb_colonnes"    : 3,
    "sauter_centre"  : True,
    "plan_pose"      : PLAN_PLATFORME,
    "pts_pose"       : [
        [0.03, 0.01, 0.003, 0.031, 0.035, 1.513], # A AJUSTER
    ],
    "ouverture_prise": 40,
    "ouverture_pose" : 47,
    "nb_par_cycle"   : 1,
    "etat_file"      : os.path.join(DOSSIER_ETATS, "etat_grille_carte_l298n.json"),
}