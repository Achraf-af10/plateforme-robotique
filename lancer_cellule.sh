#!/bin/bash
#
# lancer_cellule.sh
# Lance automatiquement toute la cellule robotique :
#   1. Le broker MQTT (mosquitto)
#   2. Le pilote UR5
#   3. Le pilote UR12e
#   4. L'orchestrateur (avec choix de l'état de départ et du mode pas-à-pas)
#
# Utilisation : ./lancer_cellule.sh
#

set -e  # arrête le script si une commande échoue

# ============================================================
# CONFIGURATION — à adapter si l'emplacement des dossiers change
# ============================================================
RACINE="$HOME/plateforme-robotique"
DOSSIER_UR5="$RACINE/pilotes/ur5"
DOSSIER_UR12E="$RACINE/pilotes/ur12e"
DOSSIER_ORCHESTRATEUR="$RACINE/orchestrateur"

SCRIPT_UR5="pilote_ur5.py"
SCRIPT_UR12E="pilote_ur12e.py"
SCRIPT_ORCHESTRATEUR="orchestrateur_principal.py"

DOSSIER_LOGS="$RACINE/logs"
VENV="$RACINE/venv/bin/activate"

# ============================================================
# COULEURS (pour un affichage plus lisible)
# ============================================================
ROUGE='\033[0;31m'
VERT='\033[0;32m'
JAUNE='\033[1;33m'
BLEU='\033[0;34m'
NEUTRE='\033[0m'

info()    { echo -e "${BLEU}[INFO]${NEUTRE} $1"; }
succes()  { echo -e "${VERT}[OK]${NEUTRE} $1"; }
attention() { echo -e "${JAUNE}[ATTENTION]${NEUTRE} $1"; }
erreur()  { echo -e "${ROUGE}[ERREUR]${NEUTRE} $1"; }

# ============================================================
# NETTOYAGE À LA SORTIE
# Si on quitte le script (Ctrl+C ou fin normale), on arrête
# proprement les pilotes lancés en arrière-plan.
# ============================================================
PID_UR5=""
PID_UR12E=""

nettoyer() {
    echo ""
    info "Arrêt en cours, fermeture des pilotes..."
    if [ -n "$PID_UR5" ] && kill -0 "$PID_UR5" 2>/dev/null; then
        kill "$PID_UR5" 2>/dev/null
        info "Pilote UR5 arrêté."
    fi
    if [ -n "$PID_UR12E" ] && kill -0 "$PID_UR12E" 2>/dev/null; then
        kill "$PID_UR12E" 2>/dev/null
        info "Pilote UR12e arrêté."
    fi
    succes "Tout est arrêté proprement."
    exit 0
}
trap nettoyer SIGINT SIGTERM

# ============================================================
# ÉTAPE 1 — Vérifications de base
# ============================================================
echo "============================================================"
echo "   Lancement de la cellule robotique"
echo "============================================================"
echo ""

if [ ! -d "$RACINE" ]; then
    erreur "Le dossier du projet n'existe pas : $RACINE"
    exit 1
fi

mkdir -p "$DOSSIER_LOGS"

# ============================================================
# ÉTAPE 1bis — Rappel checklist manuelle avant de démarrer
# ============================================================
echo "------------------------------------------------------------"
attention "Avant de continuer, vérifie que :"
echo "    1) Le dossier etats_json est bien nettoyé (anciens états supprimés)"
echo "    2) Les bacs de vis sont rechargés"
echo "    3) Les entretoises sont rechargées"
echo "    4) Les autres consommables nécessaires au cycle sont en place"
echo "------------------------------------------------------------"
echo ""
read -p "Appuie sur Entrée une fois que c'est fait, pour continuer... " _

echo ""

# ============================================================
# ÉTAPE 2 — Démarrage du broker MQTT
# ============================================================
info "Démarrage du broker MQTT (mosquitto)..."

if systemctl is-active --quiet mosquitto.service; then
    succes "Le broker MQTT tourne déjà."
else
    sudo systemctl start mosquitto.service
    sleep 1
    if systemctl is-active --quiet mosquitto.service; then
        succes "Broker MQTT démarré."
    else
        erreur "Impossible de démarrer mosquitto. Vérifie son installation."
        exit 1
    fi
fi

# ============================================================
# ÉTAPE 3 — Activation de l'environnement virtuel Python
# ============================================================
if [ -f "$VENV" ]; then
    source "$VENV"
    succes "Environnement virtuel Python activé."
else
    attention "Environnement virtuel introuvable à $VENV — on continue avec le python système."
fi

# ============================================================
# ÉTAPE 4 — Lancement des pilotes robots (en arrière-plan)
# ============================================================
info "Démarrage du pilote UR5..."
(cd "$DOSSIER_UR5" && python "$SCRIPT_UR5" > "$DOSSIER_LOGS/ur5.log" 2>&1) &
PID_UR5=$!
sleep 1

if kill -0 "$PID_UR5" 2>/dev/null; then
    succes "Pilote UR5 démarré (PID $PID_UR5). Logs : $DOSSIER_LOGS/ur5.log"
else
    erreur "Le pilote UR5 n'a pas démarré. Vérifie $DOSSIER_LOGS/ur5.log"
    exit 1
fi

info "Démarrage du pilote UR12e..."
(cd "$DOSSIER_UR12E" && python "$SCRIPT_UR12E" > "$DOSSIER_LOGS/ur12e.log" 2>&1) &
PID_UR12E=$!
sleep 1

if kill -0 "$PID_UR12E" 2>/dev/null; then
    succes "Pilote UR12e démarré (PID $PID_UR12E). Logs : $DOSSIER_LOGS/ur12e.log"
else
    erreur "Le pilote UR12e n'a pas démarré. Vérifie $DOSSIER_LOGS/ur12e.log"
    exit 1
fi

echo ""
succes "Les deux robots sont prêts et connectés au broker."
echo ""

# ============================================================
# ÉTAPE 5 — Questions à l'utilisateur pour l'orchestrateur
# ============================================================
echo "============================================================"
echo "   Configuration du cycle de production"
echo "============================================================"
echo ""

# --- Liste des états disponibles avec un libellé clair pour l'utilisateur ---
# Format : "nom_etat_technique|Description compréhensible"
ETATS_DISPONIBLES=(
    "idle|Depuis le début (cycle complet)"
    "ur12e_vers_a|Vissage entretoises PICO"
    "ur12e_vers_b|Vissage entretoises L298N"
    "ur5_vers_1|Pose de la bride moteur"
    "ur12e_vers_2|Vissage de la bride moteur"
    "ur5_vers_3|Pose du support PICO"
    "ur12e_vers_4|Vissage du support PICO"
    "ur5_vers_5|Pose du support L298N"
    "ur12e_vers_6|Vissage du support L298N"
    "ur12e_vers_8|Vissage entretoises Raspberry Pi"
    "ur5_vers_9|Pose du support 1 Raspberry Pi"
    "ur12e_vers_10|Vissage du support 1 Raspberry Pi"
    "ur5_vers_11|Pose du support 2 Raspberry Pi"
    "ur12e_vers_12|Vissage du support 2 Raspberry Pi"
    "ur5_vers_13|Pose du support powerbank"
    "ur12e_vers_14|Vissage du support powerbank"
)

echo "À quelle étape veux-tu démarrer le cycle ?"
echo ""
i=0
for entree in "${ETATS_DISPONIBLES[@]}"; do
    LIBELLE="${entree#*|}"
    echo "  $i) $LIBELLE"
    i=$((i + 1))
done
echo ""
read -p "Ton choix (numéro) : " CHOIX_ETAT

if [[ "$CHOIX_ETAT" =~ ^[0-9]+$ ]] && [ "$CHOIX_ETAT" -ge 0 ] && [ "$CHOIX_ETAT" -lt "${#ETATS_DISPONIBLES[@]}" ]; then
    ENTREE_CHOISIE="${ETATS_DISPONIBLES[$CHOIX_ETAT]}"
    ETAT_DEPART="${ENTREE_CHOISIE%%|*}"
    LIBELLE_CHOISI="${ENTREE_CHOISIE#*|}"
else
    attention "Choix invalide, démarrage depuis le début par défaut."
    ETAT_DEPART="idle"
    LIBELLE_CHOISI="Depuis le début (cycle complet)"
fi

echo ""
succes "Étape de départ choisie : $LIBELLE_CHOISI"
echo ""

# --- Mode pas-à-pas : toujours activé ---
PAS_A_PAS="1"
succes "Mode pas-à-pas activé (toujours actif)."

echo ""
echo "============================================================"
echo "   Lancement de l'orchestrateur"
echo "============================================================"
echo ""
info "État de départ : $ETAT_DEPART"
info "Mode pas-à-pas : $([ "$PAS_A_PAS" == "1" ] && echo "activé" || echo "désactivé")"
echo ""
attention "Appuie sur Ctrl+C à tout moment pour tout arrêter proprement."
echo ""
sleep 1

# ============================================================
# ÉTAPE 6 — Lancement de l'orchestrateur (au premier plan)
# ============================================================
cd "$DOSSIER_ORCHESTRATEUR"
ETAT_DEPART="$ETAT_DEPART" PAS_A_PAS="$PAS_A_PAS" python "$SCRIPT_ORCHESTRATEUR"

# Si l'orchestrateur se termine normalement (cycle fini), on nettoie aussi.
nettoyer