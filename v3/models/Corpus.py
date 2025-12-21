"""!
# Corpus.py

Module contenant la logique de gestion du corpus de documents.

**Author:** LOREL Guillaume  
**Version:** 3.0
"""

import pandas as pd
import re
from models.Author import Author
from collections import Counter

def singleton(cls):
    """!
    Décorateur pour implémenter le patron Singleton.

    **Parameters**
    - **cls**: La classe à décorer.

    **Returns**
    - Une fonction wrapper retournant l'instance unique de la classe.
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
    # Corpus

    Classe principale gérant la collection de documents et d'auteurs.

    **Note:** Utilise le pattern Singleton.
    """
    def __init__(self, nom="Corpus par défaut", documents=None, id_document=0, authors=None):
        """!
        Constructeur du Corpus.

        **Parameters**
        - **nom**: Nom du corpus.
        - **documents**: Dictionnaire initial des documents (optionnel).
        - **id_document**: Identifiant initial pour les documents (optionnel).
        - **authors**: Dictionnaire initial des auteurs (optionnel).
        """
        self.nom = nom
        self.documents = documents if documents is not None else {}
        self.authors = authors if authors is not None else {}
        self.id_document = len(self.documents) if documents is not None else id_document
        self._full_text = None
    
    def get_nom(self):
        """!
        Accesseur pour le nom du corpus.

        **Returns**
        - Le nom du corpus.
        """
        return self.nom
    
    def get_documents(self):
        """!
        Accesseur pour les documents.

        **Returns**
        - Dictionnaire des documents.
        """
        return self.documents
    
    def get_id_document(self):
        """!
        Accesseur pour l'identifiant du document.

        **Returns**
        - L'identifiant actuel pour les documents.
        """
        return self.id_document
    
    def get_authors(self):
        """!
        Accesseur pour les auteurs.

        **Returns**
        - Dictionnaire des auteurs.
        """
        return self.authors
    
    def add_document(self, document):
        """!
        Ajoute un Document au corpus et met à jour l'objet Author correspondant.

        **Parameters**
        - **document**: Instance de Document (ou classe fille) à ajouter.
        """
        self.documents[self.id_document] = document
        self.id_document += 1

        author_name = document.get_auteur()

        if author_name not in self.authors:
            self.authors[author_name] = Author(author_name, 0, []) 
        
        self.authors[author_name].add(document)

    def add_author(self, author):
        """!
        Ajoute manuellement un auteur au corpus.

        **Parameters**
        - **author**: Instance de Author à ajouter.
        """
        self.authors[author.get_nom()] = author

    def __repr__(self):
        """!
        Représentation textuelle du corpus.

        **Returns**
        - Résumé du contenu du corpus.
        """
        nb_docs = len(self.documents)
        nb_authors = len(self.authors)
        return (f"<Corpus(nom='{self.get_nom()}', docs={nb_docs}, "
                f"auteurs={nb_authors}, id_max={self.id_document - 1 if self.id_document > 0 else -1})>")
    
    def get_sorted_by_date(self, n=10):
        """!
        Affiche les 'n' documents triés par date (récent -> ancien).

        **Parameters**
        - **n**: Nombre de documents à afficher.
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
        Affiche les 'n' documents triés par titre alphabétique.

        **Parameters**
        - **n**: Nombre de documents à afficher.
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
        Enregistre le corpus sur le disque au format CSV.

        **Parameters**
        - **filename**: Nom du fichier de sauvegarde.
        """
        path = f'./v3/data/{filename}'
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
        Charge un corpus depuis un fichier CSV.

        **Parameters**
        - **filename**: Nom du fichier à charger.
        - **nom**: Nouveau nom pour le corpus chargé.
        """
        path = f'./v3/data/{filename}'
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
        Affiche les types des 'n' premiers documents du corpus.

        **Parameters**
        - **n**: Nombre de documents à afficher.
        """
        print(f"\n--- Types des documents dans le corpus '{self.nom}' ---")
        # Affiche seulement les n premiers pour éviter de polluer la console
        for doc_id, doc in list(self.documents.items())[:n]:
            print(f"ID {doc_id}: Type = {doc.getType()}")

    def search(self, keyword):
        """!
        Recherche un mot-clé dans le corpus et retourne les extraits correspondants.

        **Parameters**
        - **keyword**: Mot-clé à rechercher.

        **Returns**
        - Liste des extraits contenant le mot-clé.
        """
        if self._full_text is None:
            self._build_full_text()
        pattern = re.compile(r".{0,40}\b" + re.escape(keyword) + r"\b.{0,40}", re.IGNORECASE)
        return pattern.findall(self._full_text)
    
    def _build_full_text(self):
        """!
        Construit la chaîne de texte complète du corpus pour les recherches.
        """
        self._full_text = " ".join(doc.get_texte() for doc in self.documents.values())

    def concorde(self, pattern, context_size=30):
        """!
        Génère une concordance pour un motif donné dans le corpus.

        **Parameters**
        - **pattern**: Motif (expression régulière) à rechercher.
        - **context_size**: Taille du contexte à extraire autour du motif.

        **Returns**
        - DataFrame avec colonnes "contexte gauche", "motif trouvé", "contexte droit".
        """
        if self._full_text is None:
            self._build_full_text()
        text = self._full_text
        
        matches = re.finditer(pattern, text, re.IGNORECASE)
        
        results = []
        
        for match in matches:
            start_index = match.start()
            end_index = match.end()
            motif = match.group()
            
            # Extraire le contexte gauche
            # Début du contexte = max(0, start_index - taille du contexte)
            context_gauche_start = max(0, start_index - context_size)
            context_gauche = text[context_gauche_start:start_index].strip()
            
            # Extraire le contexte droit
            # Fin du contexte = min(longueur totale, end_index + taille du contexte)
            context_droit_end = min(len(text), end_index + context_size)
            context_droit = text[end_index:context_droit_end].strip()
            
            results.append({
                "contexte gauche": context_gauche,
                "motif trouvé": motif,
                "contexte droit": context_droit
            })
        
        if not results:
            print(f"Aucune occurrence du motif '{pattern}' trouvée.")
            return pd.DataFrame(columns=["contexte gauche", "motif trouvé", "contexte droit"])
            
        concordancier = pd.DataFrame(results)
        return concordancier
    
    def nettoyer_texte(self, text):
        """!
        Nettoie le texte en appliquant plusieurs transformations.

        **Parameters**
        - **text**: Texte brut à nettoyer.

        **Returns**
        - Texte nettoyé (minuscules, caractères non alphabétiques retirés, espaces normalisés).
        """
        text = text.lower()
        
        text = text.replace('\n', ' ')
        
        # [^a-z] signifie "tout ce qui n'est pas une lettre minuscule"
        text = re.sub(r'[^a-z\s]+', ' ', text)
        
        # Remplacement des espaces multiples par un seul espace
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    def stats(self, n=10):
        """!
        Calcule et affiche des statistiques globales et textuelles du corpus.

        **Parameters**
        - **n**: Nombre de mots les plus fréquents à afficher.

        **Returns**
        - DataFrame trié par fréquence décroissante (TF).
        """
        print(f"\n--- Statistiques du corpus '{self.nom}' ---")
        print(f"Nombre de documents: {len(self.documents)}")
        print(f"Nombre d'auteurs: {len(self.authors)}")
        print("\nStats textuelles :")
        
        # Dictionnaire pour stocker les occurrences globales (Term Frequency)
        word_counts = {} 
        
        # Dictionnaire pour stocker les documents contenant chaque mot (Document Frequency)
        doc_word_set = {}
        
        all_words = []

        for doc in self.documents.values():
            text_nettoye = self.nettoyer_texte(doc.get_texte())
            
            mots_du_doc = text_nettoye.split(' ')
            
            mots_uniques_du_doc = set(mots_du_doc)
            
            for mot in mots_uniques_du_doc:
                if mot:
                    doc_word_set[mot] = doc_word_set.get(mot, 0) + 1
            
            # Ajout des mots pour le calcul de la fréquence totale (TF)
            all_words.extend(mots_du_doc)

        
        # Utilisation d'un dictionnaire pour compter la fréquence (plus rapide que boucler à la main)
        word_counts = Counter([word for word in all_words if word])

        df_freq = pd.DataFrame(word_counts.items(), columns=['Mot', 'Term Frequency (TF)'])
        
        df_freq['Document Frequency (DF)'] = df_freq['Mot'].apply(lambda mot: doc_word_set.get(mot, 0))
        
        print(f"1. Nombre de mots différents dans le corpus (Vocabulaire): {len(word_counts)} mots.") 
        
        print(f"\n2. {n} mots les plus fréquents (Term Frequency, TF) :")
        
        # Tri par Term Frequency et affichage des n premiers
        df_freq_sorted = df_freq.sort_values(by='Term Frequency (TF)', ascending=False)
        
        print(df_freq_sorted.head(n))
        
        return df_freq_sorted