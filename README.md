# ♟️ Application de gestion de tournoi d'échecs (MVC)

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python)![Status](https://img.shields.io/badge/statut-en%20cours-yellow)![License](https://img.shields.io/badge/Licence-MIT-green)

## 📝 Description

Cette application permet de gérer des tournois d'échecs hors-ligne en utilisant l'architecture MVC. Elle gère les joueurs, les tournois, les rounds, les matchs, et assure la persistance des données via des fichiers JSON.

## 📁 Structure

```
project/
│
├── controllers/
│   └── main_controller.py
│
├── models/
│   ├── player.py
│   ├── tournament.py
│   ├── round.py
│   └── match.py
│
├── views/
│   └── main_menu.py
│
├── utils/
│   └── storage.py
│
├── data/
│   ├── players.json
│   └── tournaments.json
│
└── main.py
```

## 🎯 Fonctionnalités

* 👤 Création et sauvegarde de joueurs
* 🏆 Création et sauvegarde de tournois
* 🔄 Génération dynamique des rounds et matchs
* 🧮 Saisie des résultats avec calcul automatique des scores
* 💾 Sauvegarde et chargement automatique de l'état dans des fichiers JSON

## ⚙️ Installation

1. Clonez le projet
2. Créez les dossiers manquants s'ils ne sont pas présents :
   ```bash
   mkdir -p data models controllers views utils
   ```
3. Placez les fichiers correspondants dans les bons dossiers (voir structure ci-dessus).

## ▶️ Lancement

Depuis la racine du projet :

```bash
python main.py
```

## 🗃️ Fichiers JSON

* `data/players.json` : contient les données des joueurs
* `data/tournaments.json` : contient les données des tournois

## 💡 Persistance

Les données sont automatiquement synchronisées avec les fichiers JSON à chaque action utilisateur afin d'éviter toute perte de données.

## 🚀 Améliorations possibles

* 🖼️ Interface graphique (Tkinter, PyQt, etc.)
* 📄 Export PDF ou CSV des résultats
* 📊 Classement ELO
