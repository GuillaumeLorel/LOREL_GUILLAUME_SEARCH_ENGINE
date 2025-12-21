"""!
@file Author.py
@brief Module gérant les auteurs du corpus.
@author LOREL Guillaume
@version 1.0
"""

class Author:
    """!
    @class Author
    @brief Classe représentant un auteur et sa production de documents.
    """

    def __init__(self, name, nb_docs, production):
        """!
        @brief Constructeur de la classe Author.
        @param name Nom de l'auteur.
        @param nb_docs Nombre initial de documents.
        @param production Liste initiale des documents (objets Document).
        """
        self.name = name
        self.nb_docs = nb_docs
        self.production = production
    
    def get_name(self):
        """!
        @brief Accesseur pour le nom.
        @return Le nom de l'auteur.
        """
        return self.name

    def get_nb_docs(self):
        """!
        @brief Accesseur pour le nombre de documents.
        @return Le nombre de documents de l'auteur.
        """
        return self.nb_docs

    def get_production(self):
        """!
        @brief Accesseur pour la production.
        @return La liste des documents de l'auteur.
        """
        return self.production
    
    def add(self, document):
        """!
        @brief Ajoute un document à la production de l'auteur.
        @param document L'instance de Document à ajouter.
        """
        self.production.append(document)
        self.nb_docs += 1

    def __str__(self):
        """!
        @brief Représentation textuelle de l'auteur.
        @return Chaîne formatée avec nom et nombre de documents.
        """
        return f"Auteur: {self.name}, Documents: {self.nb_docs}"
    
    def get_average_size(self):
        """!
        @brief Calcule la taille moyenne des documents de l'auteur.
        @return La taille moyenne en caractères (float).
        """
        if self.nb_docs == 0:
            return 0
        
        # Somme des longueurs de tous les textes / nombre de docs
        total_size = sum(len(doc.get_texte()) for doc in self.production)
        return total_size / self.nb_docs
