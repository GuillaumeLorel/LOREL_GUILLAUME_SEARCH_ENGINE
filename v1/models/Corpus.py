"""!
@file Corpus.py
@brief Module contenant la logique de gestion du corpus de documents.
@author LOREL Guillaume
@version 1.0
"""

import pandas as pd
from models.Author import Author

def singleton(cls):
    """!
    @brief Décorateur pour implémenter le patron Singleton.
    @param cls La classe à décorer.
    @return L'instance unique de la classe.
    """
    instance = [None]
    def wrapper(*args, **kwargs):
        if instance[0] is None:
            instance[0] = cls(*args, **kwargs)
        return instance[0]
    return wrapper

@singleton
class Corpus:
    """!
    @class Corpus
    @brief Classe principale gérant la collection de documents et d'auteurs.
    @note Utilise le pattern Singleton.
    """
    def __init__(self, nom="Corpus par défaut", documents=None, id_document=0, authors=None):
        """!
        @brief Constructeur du Corpus.
        @param nom Nom du corpus.
        @param documents Dictionnaire initial des documents (optionnel).
        @param id_document Identifiant initial pour les documents (optionnel).
        @param authors Dictionnaire initial des auteurs (optionnel).
        """
        self.nom = nom
        self.documents = documents if documents is not None else {}
        self.authors = authors if authors is not None else {}
        self.id_document = len(self.documents) if documents is not None else id_document
    
    def get_nom(self):
        """!
        @brief Accesseur pour le nom du corpus.
        @return Le nom du corpus.
        """
        return self.nom
    
    def get_documents(self):
        """!
        @brief Accesseur pour les documents.
        @return Dictionnaire des documents.
        """
        return self.documents
    
    def get_id_document(self):
        """!
        @brief Accesseur pour l'identifiant du document.
        @return L'identifiant actuel pour les documents.
        """
        return self.id_document
    
    def get_authors(self):
        """!
        @brief Accesseur pour les auteurs.
        @return Dictionnaire des auteurs.
        """
        return self.authors
    
    def add_document(self, document):
        """!
        @brief Ajoute un Document au corpus et met à jour l'objet Author correspondant.
        @param document Instance de Document (ou classe fille) à ajouter.
        """
        self.documents[self.id_document] = document
        self.id_document += 1

        author_name = document.get_auteur()

        if author_name not in self.authors:
            self.authors[author_name] = Author(author_name, 0, []) 
        
        self.authors[author_name].add(document)

    def add_author(self, author):
        """!
        @brief Ajoute manuellement un auteur au corpus.
        @param author Instance de Author à ajouter.
        """
        self.authors[author.get_nom()] = author

    def __repr__(self):
        """!
        @brief Représentation textuelle du corpus.
        @return Résumé du contenu du corpus.
        """
        nb_docs = len(self.documents)
        nb_authors = len(self.authors)
        return (f"<Corpus(nom='{self.get_nom()}', docs={nb_docs}, "
                f"auteurs={nb_authors}, id_max={self.id_document - 1 if self.id_document > 0 else -1})>")
    
    def stats(self):
        """!
        @brief Affiche les statistiques globales du corpus.
        """
        print(f"\n--- Statistiques du corpus '{self.nom}' ---")
        print(f"Nombre de documents: {len(self.documents)}")
        print(f"Nombre d'auteurs: {len(self.authors)}")
        
    def get_sorted_by_date(self, n=10):
        """!
        @brief Affiche les 'n' documents triés par date (récent -> ancien).
        @param n Nombre de documents à afficher.
        """
        print(f"\n--- {n} documents les plus récents de {self.nom} ---")
        sorted_docs = sorted(
            self.documents.values(), 
            key=lambda doc: doc.get_date(), 
            reverse=True
        )   
        for i, doc in enumerate(sorted_docs[:n]):
            print(f"[{i + 1}] {doc}")

    def get_sorted_by_title(self, n=10):
        """!
        @brief Affiche les 'n' documents triés par titre alphabétique.
        @param n Nombre de documents à afficher.
        """
        print(f"\n--- {n} documents triés par titre de {self.nom} ---")
        sorted_docs = sorted(
            self.documents.values(), 
            key=lambda doc: doc.get_titre().lower()
        )  
        for i, doc in enumerate(sorted_docs[:n]):
            print(f"[{i + 1}] {doc}")

    def save(self, filename='corpus.csv'):
        """!
        @brief Enregistre le corpus sur le disque au format CSV.
        @param filename Nom du fichier de sauvegarde.
        """
        path = f'./v1/data/{filename}'
        print(f"\n-> Sauvegarde du corpus dans {path}...")
        
        doc_objects = list(self.documents.values())
        
        df = pd.DataFrame({
            'id': range(len(doc_objects)),
            'titre': [d.get_titre() for d in doc_objects],
            'auteur': [d.get_auteur() for d in doc_objects],
            'date': [d.get_date() for d in doc_objects],
            'url': [d.get_url() for d in doc_objects],
            'texte': [d.get_texte() for d in doc_objects],
            'type': [d.getType() for d in doc_objects],
            'nb_comments': [getattr(d, 'nb_comments', 0) for d in doc_objects],
            'co_auteurs': [str(getattr(d, 'co_auteurs', [])) for d in doc_objects] 
        })
            
        df.to_csv(path, sep='\t', index=False)
        print("Sauvegarde terminée.")

    def load(self, filename='corpus.csv', nom="Corpus Chargé"):
        """!
        @brief Charge un corpus depuis un fichier CSV.
        @param filename Nom du fichier à charger.
        @param nom Nouveau nom pour le corpus chargé.
        """
        path = f'./v1/data/{filename}'
        print(f"\n-> Chargement du corpus depuis {path}...")

        try:
            df = pd.read_csv(path, sep='\t')
        except FileNotFoundError:
            print("Erreur : Fichier non trouvé.")
            return

        self.nom = nom
        self.documents = {}
        self.authors = {}
        self.id_document = 0
        
        self.df_data = df
        
        print(f"Chargement terminé. {len(self.df_data)} lignes de données chargées.")
    
    def display_types(self, n=10):
        """!
        @brief Affiche le type de chaque document présent dans le corpus.
        """
        print(f"\n--- Types des documents dans le corpus '{self.nom}' ---")
        # Affiche seulement les n premiers pour éviter de polluer la console
        for doc_id, doc in list(self.documents.items())[:n]:
            print(f"ID {doc_id}: Type = {doc.getType()}")