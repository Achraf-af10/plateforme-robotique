# config_ur5.py
# Fichier de configuration — modifier uniquement ce fichier

# Plans recuperes automatiquement depuis le UR5
# Ne pas modifier manuellement — utiliser get_plan_ur5.py

PLAN_L298N = [
    0.415903306268062, -0.07486306829076779, 0.05465168074659954,
    -0.008131726064734859, 0.017557777516270336, 0.0054037504545519964
]

PLAN_SUP_L298N = [
    0.2562467641138699, 0.09920256668604434, 0.055536531126466615,
    -0.0019555601837086723, 0.013505038736854977, -0.002841691350030972
]

PLAN_BRIDE = [
    0.2563598750350642, -0.3273909117038984, 0.05520876180801251,
    -0.003412665908788886, 0.010066900703302767, 0.007294522318518194
]

PLAN_RASPICO = [
    0.272262598728248, -0.09052280840919583, 0.05644844971717855,
    -0.005162769265000687, 0.016353342367265992, -0.00030046083438544486
]

PLAN_SUP1_RASPI = [
    0.44696745719701236, 0.1094156381029779, 0.05389176556424652,
    -0.01934341140814349, 0.0166623448550298, -0.010560650648341465
]

PLAN_SUP2_RASPI = [
    0.5418029391239041, 0.1104409937493441, 0.05141458056262299,
    -0.0009514948178343949, 0.0019357807367525546, -0.017003141162686693
]

PLAN_SUP_PICO = [
    0.35276375251640946, 0.12889604756514322, 0.0549147599521477,
    -0.013843029690566685, 0.012922776532877236, 0.0010137306167365115
]

PLAN_DESSOUS = [
    0.2112721411868312, 0.6959759490037689, 0.1413041916305522,
    -2.202032924142858, 2.236323032983556, 0.000479078094893015
]

PLAN_DESSUS = [
    -0.07738892688247738, 0.6995597621960921, 0.13452491514305923,
    -2.220029598242967, 2.221592380709402, -0.02597228620567457
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
    "pt_prise"       : [0.03451, 0.06421, 0.03822, 2.317, -2.154, 0.047],
    "plan_pose"      : PLAN_DESSOUS,
    "pt_pose"        : [0.010, 0.150, 0.0047, 0.022,0.022,-0.070],
    "ouverture_prise": 40,
    "ouverture_pose" : 47,
    "etat_file"      : os.path.join(DOSSIER_ETATS, "etat_pile_support_pico.json"),
    "nb_support"     : NBR_SUPPORT_PICO,
}

SUPPORT_L298N = {
    "nom"            : "Support L298N",
    "plan_prise"     : PLAN_SUP_L298N,
    "pt_prise"       : [0.03416, 0.10792, 0.03986, 2.323, -2.170, 0.048],#
    "plan_pose"      : PLAN_DESSOUS,
    "pt_pose"        : [0.080, 0.150, 0.0047, 0.033,-0.002,-0.064],
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
    "pt_origine"     : [0.024,0.045,0.012,2.319,-2.181,0.022],
    "pas_x"          : 0.096,
    "pas_y"          : 0.087,
    "nb_lignes"      : 2,
    "nb_colonnes"    : 2,
    "sauter_centre"  : False,
    "plan_pose"      : PLAN_DESSOUS,
    "pts_pose"       : [
        [0.00226,0.09022,-0.00975,0.028,0.038,1.514],
        [0.15763,0.08900,-0.00975,0.026,-0.0071,-1.658], 
    ],
    "ouverture_prise": 50,
    "ouverture_pose" : 55, 
    "nb_par_cycle"   : 2,
    "etat_file"      : os.path.join(DOSSIER_ETATS, "etat_grille_bride_moteur.json"),
}

CARTE_L298N = {
    "nom"            : "Carte L298N",
    "plan_prise"     : PLAN_L298N,        
    "pt_origine"     : [0.0, 0.0, -0.017, 2.335, -2.196, 0.055],
    "pas_x"          : 0.025,
    "pas_y"          : 0.025,
    "nb_lignes"      : 3,
    "nb_colonnes"    : 3,
    "sauter_centre"  : True,
    "plan_pose"      : PLAN_DESSOUS,
    "pts_pose"       : [
        [0.080,0.150,0.00192,0.023,-0.012,-0.058],
    ],
    "ouverture_prise": 53,
    "ouverture_pose" : 54,
    "nb_par_cycle"   : 1,
    "etat_file"      : os.path.join(DOSSIER_ETATS, "etat_grille_carte_l298n.json"),
}