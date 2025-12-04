"""!
@file SearchEngine.py
@brief Moteur de recherche (Implémentation TD7).
@author LOREL Guillaume
@version 1.0
"""

import math
import numpy as np
import pandas as pd
from scipy.sparse import csr_matrix
from numpy.linalg import norm
from scipy.sparse import diags


class SearchEngine:
    """!
    @class SearchEngine
    @brief Classe gérant la matrice TF-IDF et la recherche.
    """

    def __init__(self, corpus):
        """!
        @brief Constructeur qui lance toutes les étapes d'indexation.
        @param corpus L'objet Corpus contenant les documents.
        """
        self.corpus = corpus
        self.vocab = {}          
        self.mat_TF = None       
        self.mat_TF_IDF = None   
        self.N_docs = len(corpus.get_documents())
        
        self._build_vocab()
        self._build_tf_matrix()
        self._build_tfidf_matrix()

    def _build_vocab(self):
        """!
        @brief Construction du vocabulaire à partir du corpus.
        """
        mots_uniques = set()
        docs = list(self.corpus.get_documents().values())

        for doc in docs:
            texte = self.corpus.nettoyer_texte(doc.get_texte())
            for mot in texte.split(' '):
                if mot:
                    mots_uniques.add(mot)
        
        liste_mots = sorted(list(mots_uniques))
        
        self.vocab = {}
        for i, mot in enumerate(liste_mots):
            self.vocab[mot] = {
                'id': i, 
                'doc_count': 0
            }
        print(f"-> Vocabulaire créé : {len(self.vocab)} mots.")

    def _build_tf_matrix(self):
        """!
        @brief Construction de la matrice Documents x Mots (TF).
        """
        rows = []
        cols = []
        data = []
        
        docs = list(self.corpus.get_documents().values())
        
        for index_doc, doc in enumerate(docs):
            texte = self.corpus.nettoyer_texte(doc.get_texte())
            mots_doc = [m for m in texte.split(' ') if m]
            
            compte_local = {}
            for mot in mots_doc:
                compte_local[mot] = compte_local.get(mot, 0) + 1
            
            # Remplissage des listes pour la matrice sparse
            for mot, count in compte_local.items():
                if mot in self.vocab:
                    index_mot = self.vocab[mot]['id']
                    
                    rows.append(index_doc)
                    cols.append(index_mot)
                    data.append(count)
                    
                    self.vocab[mot]['doc_count'] += 1
        
        n_vocab = len(self.vocab)
        self.mat_TF = csr_matrix((data, (rows, cols)), shape=(self.N_docs, n_vocab))

    def _build_tfidf_matrix(self):
        """!
        @brief Construction de la matrice TF-IDF.
        """
        idf_list = []
        mots_tries = sorted(self.vocab.keys())
        
        for mot in mots_tries:
            df = self.vocab[mot]['doc_count']
            # Formule IDF 
            if df > 0:
                val_idf = math.log(self.N_docs / df)
            else:
                val_idf = 0
            idf_list.append(val_idf)
            
        # Multiplication : Matrice TF * Diagonale des IDF
        diag_idf = diags(idf_list)
        
        self.mat_TF_IDF = self.mat_TF.dot(diag_idf)

    def search(self, query, n_results=10):
        """!
        @brief Recherche des documents les plus pertinents pour une requête.
        @param query La requête utilisateur.
        @param n_results Nombre de documents à retourner.
        @return Un DataFrame avec les résultats.
        """
        query_clean = self.corpus.nettoyer_texte(query)
        mots_query = [m for m in query_clean.split(' ') if m]
        
        query_vec = np.zeros(len(self.vocab))
        
        for mot in mots_query:
            if mot in self.vocab:
                idx = self.vocab[mot]['id']
                query_vec[idx] += 1 
        
        scores = []
        docs = list(self.corpus.get_documents().values())
        
        # Norme du vecteur requête ||B||
        norm_query = np.linalg.norm(query_vec)
        
        if norm_query == 0:
            return pd.DataFrame()

        # Boucle sur chaque document
        for i in range(self.N_docs):
            # On récupère le vecteur du document i
            doc_vec = self.mat_TF_IDF.getrow(i).toarray()[0]
            
            # Produit scalaire A . B
            dot_product = np.dot(doc_vec, query_vec)
            
            # Norme du document ||A||
            norm_doc = np.linalg.norm(doc_vec)
            
            if norm_doc > 0:
                sim = dot_product / (norm_doc * norm_query)
            else:
                sim = 0
            
            scores.append(sim)
            
        indices_tries = np.argsort(scores)[::-1]
        
        resultats = []
        for i in indices_tries[:n_results]:
            if scores[i] > 0:
                doc_obj = docs[i]
                resultats.append({
                    "Document": doc_obj.get_titre(),
                    "Score": round(scores[i], 4),
                    "Auteur": doc_obj.get_auteur(),
                    "Type": doc_obj.getType()
                })
                
        return pd.DataFrame(resultats)