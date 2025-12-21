# Projet Programmation Python - Moteur de Recherche

**Cours :** Programmation Python (Master 1 Informatique, Université Lyon 2)
**Auteur :** Guillaume Lorel

## Description

Ce projet implémente un moteur de recherche textuel en Python. Il a été réalisé en suivant le cycle de vie complet d'une application (spécifications, analyse, conception, tests) et se décline en trois versions évolutives.

## Structure du projet

Le code est organisé en trois dossiers correspondant aux étapes de développement :

- **v1** : Socle de base de l'application (Classes Document, Corpus, Author). Correspond aux TDs 3 à 5.
- **v2** : Implémentation du moteur de recherche et optimisations (structures de données). Correspond aux TDs 3 à 7.
- **v3** : Interface utilisateur interactive et extensions. Correspond aux TDs 3 à 10.
- **docs** : Documentation technique générée par Doxygen.

## Installation

Le projet est conçu pour fonctionner sous **Python 3.10**.

1.  Cloner le dépôt.
2.  Installer les librairies nécessaires (pandas, ipywidgets, etc.) :
    ```bash
    pip install -r requirements.txt
    ```

## Utilisation

- **Versions 1 et 2** (Console) :
  Exécuter le fichier principal de la version souhaitée :

  ```bash
  python v1/main.py
  python v2/main.py
  ```

- **Version 3** (Interface Graphique) :
  L'interface de recherche est implémentée via un Notebook Jupyter.
  Lancer Jupyter et ouvrir le fichier :
  `v3/search_engine.ipynb`

## Documentation

La documentation complète des classes et méthodes est disponible en ligne via GitHub Pages :

[Lien vers la documentation technique](https://guillaumelorel.github.io/LOREL_GUILLAUME_SEARCH_ENGINE/)

Elle est également consultable en local en ouvrant le fichier `docs/index.html`.
