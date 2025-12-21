# Moteur de Recherche Python

Projet académique d'implémentation d'un moteur de recherche en Python pour le cours de Programmation de Spécialité (UE53) à l'Université Lyon 2.

## 📋 Description du Projet

Ce projet développe progressivement un moteur de recherche capable de :

- Indexer et rechercher des documents
- Gérer plusieurs sources de données (arXiv, Reddit, etc.)
- Optimiser les performances à travers les versions
- Fournir une interface interactive avec Jupyter

## 📂 Structure du Projet

```
├── v1/              # Version 1 : Implémentation initiale
├── v2/              # Version 2 : Améliorations et optimisations
├── v3/              # Version 3 : Intégration Jupyter
├── docs/            # Documentation Doxygen
├── Doxyfile         # Configuration Doxygen
├── README.md        # Ce fichier
└── .gitignore       # Configuration Git
```

### Versions

**V1 - Implémentation Basique**

- Structure de base des classes (Document, Corpus, Author)
- Indexation simple des documents
- Fonctions de recherche élémentaires

**V2 - Optimisations**

- Amélioration des performances
- Optimisation des structures de données
- Meilleure gestion des corpus volumineux

**V3 - Interface Interactive**

- Intégration avec Jupyter Notebook
- Interface interactive pour l'exploration
- Documentation complète du processus

## 🚀 Démarrage Rapide

### Prérequis

- Python 3.8+
- pip (gestionnaire de paquets)
- Jupyter Notebook (optionnel pour v3)

### Installation

```bash
# Cloner le projet
git clone <url-repo>
cd LOREL_GUILLAUME_SEARCH_ENGINE

# Installer les dépendances
pip install -r requirements.txt
```

### Exécution

```bash
# Version 1
python v1/main.py

# Version 2
python v2/main.py

# Version 3
jupyter notebook v3/search_engine.ipynb
```

## 📖 Documentation

La documentation API complète est disponible dans le dossier `docs/`:

- Générer la documentation : `doxygen Doxyfile`
- Consulter en ligne : `docs/html/index.html`

Les pages GitHub déploient automatiquement la documentation.

## 🏗️ Architecture

### Classes Principales

**Document**

- Classe de base pour les documents
- Attributs : titre, contenu, URL, date

**Corpus**

- Gère une collection de documents
- Indexation et recherche

**Author**

- Information sur les auteurs
- Gestion des métadonnées

**ArxivDocument** (V2+)

- Spécialisation pour articles arXiv
- Extraction des métadonnées arXiv

**RedditDocument** (V2+)

- Spécialisation pour posts Reddit
- Gestion des discussions

## 🔍 Utilisation

### Exemple Basique

```python
from v1.main import Corpus, Document

# Créer un corpus
corpus = Corpus()

# Ajouter des documents
doc = Document("Python", "Langage de programmation...")
corpus.add(doc)

# Rechercher
results = corpus.search("programmation")
```

### Recherche Avancée (V2+)

```python
# Avec filtres
results = corpus.search("machine learning", max_results=10)

# Recherche avec pagination
for page in corpus.search_paginated("deep learning", page_size=5):
    print(page)
```

## 📊 Caractéristiques

- ✅ Indexation efficace des documents
- ✅ Recherche multi-termes
- ✅ Support de plusieurs sources (arXiv, Reddit)
- ✅ Interface Jupyter interactive
- ✅ Documentation API complète
- ✅ Tests et validation

## 🛠️ Technologie

- **Langage** : Python 3.8+
- **Documentation** : Doxygen
- **Déploiement** : GitHub Pages
- **Notebooks** : Jupyter

## 📝 Licence

Projet universitaire - Université Lyon 2

## 👤 Auteur

Guillaume Lorel

## 📞 Support

Pour toute question, consultez la documentation ou les commentaires du code.

---

**Générée avec Doxygen** | [Voir la documentation](docs/html/index.html)
