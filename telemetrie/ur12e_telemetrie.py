# Importe la fonction de télémétrie des robots UR
from commun_ur import lancer_telemetrie_ur

if __name__ == "__main__":
    # Lance la télémétrie du UR12e
    lancer_telemetrie_ur(nom="ur12e", ip="10.120.0.12", fichier_energie="energie_cumulee_ur12e.json")