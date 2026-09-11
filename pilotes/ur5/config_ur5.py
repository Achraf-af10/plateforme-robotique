# config_ur5.py
# Fichier de configuration — modifier uniquement ce fichier

# Plans recuperes automatiquement depuis le UR5
# Ne pas modifier manuellement — utiliser get_plan_ur5.py

# repere carte de puissance 
PLAN_L298N = [
    0.415903306268062, -0.07486306829076779, 0.05465168074659954,
    -0.008131726064734859, 0.017557777516270336, 0.0054037504545519964
]

# repere support/bac carte de puissance 
PLAN_SUP_L298N = [
    0.2562467641138699, 0.09920256668604434, 0.055536531126466615,
    -0.0019555601837086723, 0.013505038736854977, -0.002841691350030972
]

# repere support/bac bride moteur
PLAN_BRIDE = [
    0.2563598750350642, -0.3273909117038984, 0.05520876180801251,
    -0.003412665908788886, 0.010066900703302767, 0.007294522318518194
]

# repere carte raspi
PLAN_RASPICO = [
    0.272262598728248, -0.09052280840919583, 0.05644844971717855,
    -0.005162769265000687, 0.016353342367265992, -0.00030046083438544486
]

# repere support/bac 1er raspi
PLAN_SUP1_RASPI = [
    0.44696745719701236, 0.1094156381029779, 0.05389176556424652,
    -0.01934341140814349, 0.0166623448550298, -0.010560650648341465
]

# repere support/bac 2eme raspi
PLAN_SUP2_RASPI = [
    0.5418029391239041, 0.1104409937493441, 0.05141458056262299,
    -0.0009514948178343949, 0.0019357807367525546, -0.017003141162686693
]

# repere support/bac pico
PLAN_SUP_PICO = [
    0.35276375251640946, 0.12889604756514322, 0.0549147599521477,
    -0.013843029690566685, 0.012922776532877236, 0.0010137306167365115
]

# repere plateforme de travail (dessous)
PLAN_DESSOUS = [
    0.21136288185795937, 0.7195272156546326, 0.14136029868392827,
    -2.1993497985184676, 2.2338882591404023, 0.004843240400947487
]

# repere plateforme de travail (dessus)
PLAN_DESSUS = [
    -0.07655154440844751, 0.723245801154086, 0.14100708746650834,
    -2.2100468075173305, 2.2310031209317103, 0.01664811514468511
]

# repere support/bac powerbank
PLAN_SUP_POWERBANK = [
    0.5514372245348925, -0.26646787136559186, 0.0542527492397433,
    -0.005961115416691898, 0.01769347385032139, 0.002110721612619694
] 

# repere carte raspi4
PLAN_RASPI4 = [
    0.6902320296656295, -0.11956113570840263, 0.05131808148261274,
    -0.004514018244157369, 0.017019741012314994, -0.0030428364174377876
]

# Position de depart
DEPART_Q = [
    2.3968450477696024e-05, -1.570796314870016, -1.57074481645693,
    -1.5707839171039026, 1.570831537246704, 5.992112710373476e-05
]
"""
PLAN_GABARIT=[0, 0, 0, 0, 0, 0]
"""

# Vitesses de mouvement
SPEED_J       = 0.5
ACC_J         = 0.8
SPEED_L_SLOW  = 0.02
ACC_L_SLOW    = 0.04
SPEED_L_RETRAIT = 0.15
ACC_L_RETRAIT   = 0.15
SPEED_L_RAPIDE = 0.25 
ACC_L_RAPIDE   = 0.5

"""
# Vitesses de mouvement
SPEED_J_AVANT     = 0.5 
SPEED_J_APRES     = 0.5 
ACC_J_AVANT       = 0.8
ACC_J_APRES     = 0.8
SPEED_L_SLOW  = 0.02
ACC_L_SLOW    = 0.04
SPEED_L_RETRAIT = 0.15 # VITESSE LINEARE DE RETRAIT APRES AVOIR POSE LA PIECE
ACC_L_RETRAIT   = 0.15 
SPEED_L_RAPIDE = 0.25 # vitesse entre point d'approche et point de prise
ACC_L_RAPIDE   = 0.5
"""

# Geometrie & Piles
EPAISSEUR_SUPPORT  = 0.0115
MARGE_DETECTION    = 0.1
MARGE_INTER = MARGE_DETECTION * 0.4 #

NBR_SUPPORT_PICO   = 5
NBR_SUPPORT_L298N  = 5
NBR_SUPPORT_1_RASPI = 5
NBR_SUPPORT_2_RASPI = 5
NBR_SUPPORT_POWERBANK = 5

# Detection de contact
MARGE_FORCE      = 15.0  # N
TIMEOUT_CONTACT  = 20.0   # s

# Pince
PINCE_FORCE = 80
PINCE_SPEED = 100

SPEED_SLIDER = 0.9 # no used

# Declaration des supports/bacs
# plan_prise / plan_pose : reperes ou sont exprimes pt_prise / pt_pose
# pt_prise, pt_pose      : [x, y, z, rx, ry, rz] dans leur repere local
# ouverture_prise/pose/fermeture_prise   : ouverture de pince (mm) a la prise / a la pose
# etat_file              : fichier JSON de suivi de pile pour ce support
# nb_support             : nombre initial de pieces dans la pile

import os

# Remonte d'un niveau pour cibler 'pilotes/etats'
DOSSIER_ETATS = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "etats_json"))
os.makedirs(DOSSIER_ETATS, exist_ok=True)

"""
SUPPORT_PICO = {
    "nom"            : "Support Pico",
    "plan_prise"     : PLAN_SUP_PICO,  #repere du support pico
    "pt_prise"       : [0.03451, 0.06421, 0.03822, 2.317, -2.154, 0.047], # point de prise du support pico dans le repere du support
    "plan_pose"      : PLAN_DESSOUS, # repere du surface en dessous de la plateforme plaque
    "pt_pose"        : [0.010, 0.150, 0.0047, 0.022,0.022,-0.070], # point de pose du support dans le repere de la plateforme
    "ouverture_prise": 40, # ouverture de la pince pour la prise
    "fermeture_prise": 0, # fermeture de la pince
    "ouverture_pose" : 47, # ouverture de la pince pour lacher la piece
    "etat_file"      : os.path.join(DOSSIER_ETATS, "etat_pile_support_pico.json"),
    "nb_support"     : NBR_SUPPORT_PICO, # le nombre du support dans le bac avant le demarrage
}
"""

SUPPORT_PICO = {
    "nom"            : "Support Pico",
    "plan_prise"     : PLAN_SUP_PICO,
    "pt_prise"       : [0.03451, 0.06421, 0.03822, 2.317, -2.154, 0.047],
    "plan_pose"      : PLAN_DESSOUS,
    "pt_pose"        : [0.010, 0.150, 0.0047, 0.022,0.022,-0.070],
    "ouverture_prise": 40,
    "fermeture_prise": 0,
    "ouverture_pose" : 47,
    "etat_file"      : os.path.join(DOSSIER_ETATS, "etat_pile_support_pico.json"),
    "nb_support"     : NBR_SUPPORT_PICO, 
}

SUPPORT_L298N = {
    "nom"            : "Support L298N",
    "plan_prise"     : PLAN_SUP_L298N,
    "pt_prise"       : [0.03416, 0.10792, 0.03986, 2.323, -2.170, 0.048],
    "plan_pose"      : PLAN_DESSOUS,
    "pt_pose"        : [0.080, 0.150, 0.0047, 0.033,-0.002,-0.064],
    "ouverture_prise": 70,
    "fermeture_prise": 0,
    "ouverture_pose" : 73,
    "etat_file"      : os.path.join(DOSSIER_ETATS, "etat_pile_support_l298n.json"),
    "nb_support"     : NBR_SUPPORT_L298N,
}

SUPPORT_SUP1_RASPI = {
    "nom"            : "Support 1 Raspi",
    "plan_prise"     : PLAN_SUP1_RASPI,
    "pt_prise"       : [0.03305, 0.09416, 0.02840, 3.213, 0.116, 0.004],
    "plan_pose"      : PLAN_DESSUS,
    "pt_pose"        : [0.130, 0.160, 0.001, 0.041,-0.040,-0.063],
    "ouverture_prise": 33,
    "fermeture_prise": 77,
    "ouverture_pose" : 33,
    "etat_file"      : os.path.join(DOSSIER_ETATS, "etat_pile_support_1_raspi.json"),
    "nb_support"     : NBR_SUPPORT_1_RASPI,
}

SUPPORT_SUP2_RASPI = {
    "nom"            : "Support 2 Raspi",
    "plan_prise"     : PLAN_SUP2_RASPI,
    "pt_prise"       : [0.03384, 0.09362, 0.01522, 3.193, 0.110, -0.029],
    "plan_pose"      : PLAN_DESSUS,
    "pt_pose"        : [0.130, 0.160, -0.006, 0.019,-0.007,-0.063],
    "ouverture_prise": 59,
    "fermeture_prise": 0,
    "ouverture_pose" : 65,
    "etat_file"      : os.path.join(DOSSIER_ETATS, "etat_pile_support_2_raspi.json"),
    "nb_support"     : NBR_SUPPORT_2_RASPI,
}

SUPPORT_SUP_POWERBANK = {
    "nom"            : "Support Powerbank",
    "plan_prise"     : PLAN_SUP_POWERBANK,
    "pt_prise"       : [-0.06190, 0.08625, 0.04010, 0.101, -3.161, 0.073],
    "plan_pose"      : PLAN_DESSUS,
    "pt_pose"        : [0.03610, 0.08445, 0.005, 0.011, -0.101, -3.194],
    "ouverture_prise": 33,
    "fermeture_prise": 77,
    "ouverture_pose" : 33,
    "etat_file"      : os.path.join(DOSSIER_ETATS, "etat_pile_support_powerbank.json"),
    "nb_support"     : NBR_SUPPORT_POWERBANK,
}

# grille
# Grille de pieces : position de depart, ecart, dimensions et centre a ignorer
# plan_prise / plan_pose : reperes pour la prise et la pose
# pts_pose : positions de pose des pieces
# ouverture_prise/pose : ouverture de la pince (mm)
# nb_par_cycle : nombre de pieces par cycle
# etat_file : fichier JSON pour sauvegarder l'avancement

"""
BRIDE_MOTEUR = {
    "nom"            : "Bride moteur",
    "plan_prise"     : PLAN_BRIDE, # repere de la grille bride moteur         
    "pt_origine"     : [0.024,0.045,0.012,2.319,-2.181,0.022], # premier point de prise dans le repere grille 
    "pas_x"          : 0.096, # l'incrementation sur laxe x
    "pas_y"          : 0.087,  # l'incrementation sur laxe y
    "nb_lignes"      : 2, # nombre d'element dans la matrice ligne
    "nb_colonnes"    : 2, # nombre d'element dans la matrice colonne
    "sauter_centre"  : False, # false : pour ne pas sauter le centre de la grille et true : pour sauter le centre
    "plan_pose"      : PLAN_DESSOUS, # repere plaque en dessous
    "pts_pose"       : [
        [0.00226,0.09022,-0.00975,0.028,0.038,1.514], # point de pose pour le 1er bride dans le repere plaque 
        [0.15641,0.09190,-0.00975,0.027,-0.007,-1.639], # point de pose pour le 2eme bride dans le repere plaque
    ],
    "ouverture_prise": 50, # ouverture de la pince pour la prise
    "fermeture_prise": 0, # fermeture de la pince
    "ouverture_pose" : 55, # ouverture de la pince pour lacher
    "nb_par_cycle"   : 2, # nombre de bride dans un meme cycle
    "etat_file"      : os.path.join(DOSSIER_ETATS, "etat_grille_bride_moteur.json"),
}
"""

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
        [0.15641,0.09190,-0.00975,0.027,-0.007,-1.639], 
    ],
    "ouverture_prise": 50,
    "fermeture_prise": 0,
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
    "fermeture_prise": 0,
    "ouverture_pose" : 54,
    "nb_par_cycle"   : 1,
    "etat_file"      : os.path.join(DOSSIER_ETATS, "etat_grille_carte_l298n.json"),
}