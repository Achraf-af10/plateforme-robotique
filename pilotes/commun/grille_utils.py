# grille_utils.py
# Utilitaires communs pour les pieces/vis organisees en grille (matrice N x M
# avec pas x/y connu). Partage par scenarios_ur5.py et scenarios_ur12e.py.

import json
import os


def positions_grille(grille):
    """
    Calcule la liste des points [x, y, z, rx, ry, rz], ligne par ligne,
    en sautant la case centrale si sauter_centre=True (grille impaire uniquement).
    Attend un dict avec : pt_origine, pas_x, pas_y, nb_lignes, nb_colonnes,
    et optionnellement sauter_centre.
    """
    origine   = grille["pt_origine"]
    pas_x     = grille["pas_x"]
    pas_y     = grille["pas_y"]
    nb_lignes = grille["nb_lignes"]
    nb_cols   = grille["nb_colonnes"]
    sauter_centre = grille.get("sauter_centre", False)

    ligne_centre = (nb_lignes - 1) / 2
    col_centre   = (nb_cols - 1) / 2

    positions = []
    for ligne in range(nb_lignes):
        for col in range(nb_cols):
            if sauter_centre and ligne == ligne_centre and col == col_centre:
                continue
            pt = [
                origine[0] + col * pas_x,
                origine[1] + ligne * pas_y,
                origine[2],
                origine[3], origine[4], origine[5],
            ]
            positions.append(pt)
    return positions


def initialiser_grille(grille):
    """Reinitialise l'indice courant de la grille (prochain element = indice 0)."""
    with open(grille["etat_file"], "w") as f:
        json.dump({"prochain_indice": 0}, f)
    print(f"[grille] Grille initialisee ({grille['nom']})")


def indice_courant_grille(grille):
    """
    Retourne le prochain indice a utiliser dans la grille. Si le fichier
    d'etat n'existe pas encore, la grille est consideree comme neuve et
    initialisee automatiquement a l'indice 0 (utile pour un pilote MQTT
    qui tourne en continu, sans etape d'initialisation manuelle prealable).
    """
    etat_file = grille["etat_file"]
    if not os.path.exists(etat_file):
        print(f"[grille] {grille['nom']} — pas d'etat trouve, initialisation automatique a l'indice 0")
        initialiser_grille(grille)
    with open(etat_file) as f:
        etat = json.load(f)
    if "prochain_indice" not in etat:
        print(f"[grille] {grille['nom']} — etat invalide, reinitialisation a l'indice 0")
        initialiser_grille(grille)
        return 0
    return etat["prochain_indice"]


def consommer_element_grille(grille):
    etat_file = grille["etat_file"]
    with open(etat_file) as f:
        etat = json.load(f)
    etat["prochain_indice"] += 1
    with open(etat_file, "w") as f:
        json.dump(etat, f)