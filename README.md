# Plateforme Robotique — Cellule Multi-Robots Industrie 4.0

Plateforme d'orchestration d'une cellule robotique multi-marques (UR5, UR12e, JAKA S5) pour une tâche d'assemblage automatisée, développée dans le cadre d'un stage de recherche au **CERI SN — IMT Nord Europe**.

> ⚠️ **Projet en cours de développement.** L'architecture, les scénarios et les scripts évoluent au fil du stage : certains modules seront complétés, réorganisés ou retirés. Ce README sera mis à jour en conséquence.

---

## 🎯 Objectif

Coordonner plusieurs robots industriels hétérogènes (bras collaboratifs UR et JAKA, à terme YuMi et KUKA iiwa) autour d'une tâche d'assemblage répétitive, en s'appuyant sur :
- une **communication découplée** entre robots via MQTT,
- un **orchestrateur central** piloté par une machine à états finis (FSM),
- une **télémétrie temps réel** (courant, tension, puissance, énergie cumulée) visualisée via Node-RED.

## 🏗️ Architecture

Le système repose sur deux flux MQTT distincts :

| Flux | Rôle | Composants |
|---|---|---|
| **Commande / orchestration** | Séquencement des tâches d'assemblage | Orchestrateur (FSM) + pilotes robots |
| **Télémétrie** | Supervision énergétique et état des axes | Scripts de télémétrie + dashboard Node-RED |

```
                    ┌────────────────────┐
                    │   Orchestrateur     │
                    │  (machine à états)  │
                    └─────────┬───────────┘
                              │ cell/robot/<robot>/cmd
                 ┌────────────┼────────────┐
                 ▼            ▼            ▼
             ┌───────┐   ┌────────┐   ┌────────┐
             │  UR5  │   │ UR12e  │   │  JAKA  │
             └───┬───┘   └───┬────┘   └───┬────┘
                 │ cell/robot/<robot>/status │
                 └────────────┴────────────┘
                              │
                    ┌─────────▼──────────┐
                    │   Broker MQTT       │
                    │   (Mosquitto)       │
                    └─────────┬──────────┘
                              │ télémétrie (courant, tension, énergie)
                    ┌─────────▼──────────┐
                    │   Dashboard         │
                    │   Node-RED          │
                    └────────────────────┘
```

L'orchestrateur pilote une séquence de 6 étapes réparties sur les robots UR5, UR12e et JAKA (prise de support, vissage, reprise, revissage), chaque robot publiant son statut (`idle`, `busy`, `done`, `error`) qui déclenche la transition suivante de la FSM.

## 📁 Structure du dépôt

```
plateforme-robotique/
├── orchestrateur/          # Orchestrateur central (FSM + logique MQTT)
│   ├── machine_etats.py
│   └── orchestrateur_principal.py
├── pilotes/                 # Pilotes MQTT par robot
│   ├── commun/               # Client MQTT générique, utilitaires
│   ├── ur5/                  # Pilote, config et scénarios UR5
│   ├── ur12e/                 # Pilote, config et scénarios UR12e
│   ├── jaka/                  # Pilote et scénarios JAKA
│   └── effecteurs/            # Contrôle des effecteurs (pince 2FG7, visseuse)
├── telemetrie/               # Scripts de télémétrie (courant/tension/énergie) par robot
├── mosquitto/config/         # Configuration du broker MQTT
├── nodered_data/             # Configuration et flows du dashboard Node-RED
├── script/                   # Scripts utilitaires (ex. URScript)
├── docker-compose.yml        # Déploiement Mosquitto + Node-RED
└── requirements.txt
```

## ⚙️ Prérequis

- Python 3.10+
- Docker et Docker Compose (pour le broker MQTT et Node-RED)
- Accès réseau aux robots (UR5, UR12e, JAKA) sur le réseau de la cellule

## 🚀 Installation

```bash
git clone https://github.com/Achraf-af10/plateforme-robotique.git
cd plateforme-robotique
pip install -r requirements.txt
```

Lancer l'infrastructure MQTT et le dashboard :

```bash
docker compose up -d
```

Le broker Mosquitto est exposé sur le port `1883` et le dashboard Node-RED sur le port `1880`.

## ▶️ Utilisation

1. **Démarrer les pilotes robots** (un par robot, chacun s'abonne à son topic de commande) :
   ```bash
   python pilotes/ur5/pilote_ur5.py
   python pilotes/ur12e/pilote_ur12e.py
   python pilotes/jaka/pilote_jaka.py
   ```
2. **Démarrer l'orchestrateur**, qui séquence les tâches et écoute les statuts :
   ```bash
   python orchestrateur/orchestrateur_principal.py
   ```
3. **Démarrer la télémétrie** (optionnel, pour la supervision énergétique) :
   ```bash
   python telemetrie/lancer_tous.py
   ```

## 📡 Convention des topics MQTT

| Topic | Direction | Contenu |
|---|---|---|
| `cell/robot/<robot>/cmd` | Orchestrateur → Robot | Tâche à exécuter (`{"task": "..."}`) |
| `cell/robot/<robot>/status` | Robot → Orchestrateur | État courant (`idle`, `busy`, `done`, `error`) |
| `<robot>/state`, `<robot>/joints` | Robot → Node-RED | Télémétrie (courant, tension, puissance, énergie cumulée) |

## 🧩 Technologies utilisées

- **Python** — `paho-mqtt`, `transitions` (FSM), `ur_rtde`, `paramiko`
- **MQTT** — Eclipse Mosquitto
- **Node-RED** — dashboard de supervision (visualisation uniquement, aucun rôle d'orchestration)
- **Docker Compose** — déploiement de l'infrastructure
- Robots : UR5, UR12e (via RTDE), JAKA S5 (via SDK `jkrc`)
- Effecteurs : pince OnRobot 2FG7, visseuse OnRobot SD, ventouse VGC10

## 🗺️ État d'avancement

- ✅ Orchestrateur FSM et pilotes UR5 / UR12e / JAKA fonctionnels sur un cycle de démonstration à 6 étapes
- ✅ Télémétrie énergétique (UR + JAKA) opérationnelle
- ✅ Dashboard Node-RED de supervision
- 🔄 Intégration ABB YuMi et KUKA iiwa (à venir)
- 🔄 Généralisation à un cycle d'assemblage réel multi-itérations

## 👤 Auteur

**Achraf** — Stage Industrie 4.0 / robotique multi-robots, CERI SN, IMT Nord Europe (avril–septembre 2026)
