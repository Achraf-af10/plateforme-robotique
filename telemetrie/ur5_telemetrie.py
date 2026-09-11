# Importe la fonction de télémétrie des robots UR
from commun_ur import lancer_telemetrie_ur

if __name__ == "__main__":
    # Lance la télémétrie du UR5
    lancer_telemetrie_ur(nom="ur5",ip="10.120.0.11",fichier_energie="energie_cumulee_ur5.json")