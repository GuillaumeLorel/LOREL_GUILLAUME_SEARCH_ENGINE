"""!
# main.py

Point d'entrée principal (v3) : constitution d'un corpus et moteur de recherche.

**Author:** LOREL Guillaume  
**Version:** 3.0

Ce script:
- récupère des documents depuis Reddit et Arxiv,
- les ajoute dans un objet `Corpus`,
- construit ensuite un `SearchEngine` (TF-IDF) pour effectuer des recherches.
"""

import urllib
import os
import praw
import xmltodict
from datetime import datetime

from models.Document import ArxivDocument, RedditDocument
from models.Corpus import Corpus
from models.SearchEngine import SearchEngine


def main():
    """!
    Exécute le pipeline complet (collecte -> corpus -> indexation -> recherche).

    Cette fonction orchestre la récupération des documents depuis Reddit et Arxiv,
    la construction du `Corpus`, puis l'initialisation et le test du `SearchEngine`.
    """
    ## @cond

    # --- Initialisation du Corpus ---
    mon_corpus = Corpus(nom="Mon Corpus de Software Engineering")
    print(f"Corpus initialisé: {mon_corpus.get_nom()}")

    # --- Récupération des données Reddit ---
    print("Récupération des données Reddit...")
    reddit = praw.Reddit(
        client_id='qEY9Nqfurw9S940i1r36BA', 
        client_secret='S5G7DTl6Vmp2qlhxDwBdN01mCFVjOA', 
        user_agent='Software Engineering Search Engine'
    )

    hot_posts = reddit.subreddit("SoftwareEngineering").hot(limit=300)
    for post in hot_posts:
        if post.selftext:
            titre = post.title
            auteur = str(post.author) if post.author else "Inconnu"
            # Ajout du 'Z' pour indiquer UTC explicitement
            date = datetime.fromtimestamp(post.created_utc).isoformat() + 'Z'
            url = post.shortlink
            texte = post.selftext.replace('\n', ' ')
            nb_comments = post.num_comments

        doc = RedditDocument(titre, auteur, date, url, texte, nb_comments)  
        mon_corpus.add_document(doc)     

    # --- Récupération des données Arxiv ---
    print("Récupération des données Arxiv...")
    url = 'http://export.arxiv.org/api/query?search_query=all:Software%20Engineering&start=0&max_results=300'
    data = urllib.request.urlopen(url).read().decode()
    parsed_data = xmltodict.parse(data)

    for entry in parsed_data['feed']['entry']:
        titre = entry.get('title', 'Sans titre').replace('\n', ' ')

        # Gestion des auteurs (un dict ou une liste de dicts)
        auteurs_data = entry.get('author', [])
        auteur = "Inconnu"
        co_auteurs = []

        if isinstance(auteurs_data, dict):
            auteur = auteurs_data.get('name', 'Inconnu')
        elif isinstance(auteurs_data, list) and auteurs_data:
            noms_auteurs = [a.get('name', 'Auteur inconnu')
                            for a in auteurs_data
                            if isinstance(a, dict)]

            if noms_auteurs:
                auteur = noms_auteurs[0]
                if len(noms_auteurs) > 1:
                    co_auteurs = noms_auteurs[1:]

        date_pub = entry.get('published', 'Date inconnue')
        url = entry.get('id', 'URL inconnue')
        texte = entry['summary'].replace('\n', ' ')

        doc = ArxivDocument(titre, auteur, date_pub, url, texte, co_auteurs=co_auteurs)
        mon_corpus.add_document(doc)

    # --- Représentation du Corpus ---
    print(mon_corpus.__repr__())

    # --- Affichage de statistiques ---
    mon_corpus.stats()

    # --- Affichage et Tri ---
    mon_corpus.get_sorted_by_date(n=3)
    mon_corpus.get_sorted_by_title(n=3)

    # --- Affichage des types de documents ---
    mon_corpus.display_types(n=5)

    # --- Statistiques par Auteur ---
    auteurs = mon_corpus.get_authors()
    if "Daniel Graziotin" in auteurs:
        auteur_obj = auteurs["Daniel Graziotin"]
        nb_docs = auteur_obj.get_nb_docs()
        moyenne = auteur_obj.get_average_size()

        print(f"\n--- Statistiques pour l'auteur '{auteur_obj.get_name()}' ---")
        print(f"- Nombre de documents : {nb_docs}")
        print(f"- Taille moyenne      : {moyenne:.2f} caractères")

    # --- Sauvegarde et Chargement ---
    NOM_FICHIER = 'corpus_data.csv'

    # Sauvegarde
    # mon_corpus.save(filename=NOM_FICHIER)

    # Chargement d'un nouveau corpus
    # corpus_charge = Corpus(nom="Nouveau Corpus Vide")
    # corpus_charge.load(filename=NOM_FICHIER, nom="Mon Corpus Chargé")

    # Recherche par mot-clé
    keyword = "design"
    results = mon_corpus.search(keyword)
    print(f"\n--- Résultats de la recherche pour le mot-clé '{keyword}' ---")
    for i, passage in enumerate(results):
        print(f"[{i + 1}] ...{passage}...")

    # Affichage tableau concorde
    concordance_results = mon_corpus.concorde(keyword, context_size=30)
    print(f"\n--- Tableau de concordance pour le mot-clé '{keyword}' ---")
    print(concordance_results)

    mon_corpus.stats(n=15)

    print("\n--- Initialisation du SearchEngine ---")
    engine = SearchEngine(mon_corpus)
    print(engine)

    print("\n--- Test du Moteur de Recherche ---")

    query_user = input("\nEntrez vos mots-clés : ")
    print(engine.search(query_user, n_results=5))

    ## @endcond


if __name__ == "__main__":
    main()