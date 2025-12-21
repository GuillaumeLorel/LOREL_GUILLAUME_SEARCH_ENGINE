"""!
@file Document.py
@brief Module contenant les classes représentant les documents (Mère et Filles).
@author LOREL Guillaume
@version 1.0
"""

class Document:
    """!
    @class Document
    @brief Classe mère représentant un document générique.
    """

    def __init__(self, titre, auteur, date, url, texte):
        """!
        @brief Constructeur de la classe Document.
        @param titre Titre du document.
        @param auteur Auteur du document.
        @param date Date de publication (format ISO).
        @param url Lien vers le document.
        @param texte Contenu textuel du document.
        """
        self.titre = titre
        self.auteur = auteur
        self.date = date
        self.url = url
        self.texte = texte
        self.type = "Inconnu"

    def get_titre(self):
        """!
        @brief Accesseur pour le titre.
        @return Le titre du document.
        """
        return self.titre

    def get_auteur(self):
        """!
        @brief Accesseur pour l'auteur.
        @return L'auteur du document.
        """
        return self.auteur

    def get_date(self):
        """!
        @brief Accesseur pour la date.
        @return La date de publication du document.
        """
        return self.date

    def get_url(self):
        """!
        @brief Accesseur pour l'URL.
        @return L'URL du document.
        """
        return self.url

    def get_texte(self):
        """!
        @brief Accesseur pour le texte.
        @return Le contenu textuel du document.
        """
        return self.texte

    def getType(self):
        """!
        @brief Accesseur pour le type de document.
        @return Le type sous forme de chaîne de caractères.
        """
        return self.type

    def __str__(self):
        """!
        @brief Représentation textuelle du document.
        @return Chaîne décrivant le document (titre).
        """
        return f"Titre du document: {self.titre}"

    def afficher_informations(self):
        """!
        @brief Affiche toutes les informations du document dans la console.
        """
        print(f"Titre: {self.titre}")
        print(f"Auteur: {self.auteur}")
        print(f"Date: {self.date}")
        print(f"URL: {self.url}")
        print(f"Texte: {self.texte}")
    

class RedditDocument(Document):
    """!
    @class RedditDocument
    @brief Classe fille représentant un post Reddit.
    @see Document
    """
    def __init__(self, titre, auteur, date, url, texte, nb_comments):
        """!
        @brief Constructeur de RedditDocument.
        @param nb_comments Nombre de commentaires du post.
        """
        super().__init__(titre=titre, auteur=auteur, date=date, url=url, texte=texte)
        self.nb_comments = nb_comments
        self.type = "Reddit"

    def get_nb_comments(self):
        """!
        @brief Accesseur pour le nombre de commentaires.
        @return Nombre de commentaires (int).
        """
        return self.nb_comments

    def getType(self):
        """!
        @brief Surcharge pour retourner le type Reddit.
        @return "Reddit".
        """
        return self.type

    def __str__(self):
        """!
        @brief Surcharge de l'affichage.
        @return Description incluant le nombre de commentaires.
        """
        return super().__str__() + f" avec {self.nb_comments} commentaires"
        

class ArxivDocument(Document):
    """!
    @class ArxivDocument
    @brief Classe fille représentant un article Arxiv.
    @see Document
    """
    def __init__(self, titre, auteur, date, url, texte, co_auteurs=None):
        """!
        @brief Constructeur d'ArxivDocument.
        @param co_auteurs Liste des co-auteurs (optionnel).
        """
        super().__init__(titre=titre, auteur=auteur, date=date, url=url, texte=texte)
        self.co_auteurs = co_auteurs if co_auteurs is not None else []
        self.type = "Arxiv"

    def get_co_auteurs(self):
        """!
        @brief Accesseur pour les co-auteurs.
        @return Liste des co-auteurs.
        """
        return self.co_auteurs
    
    def set_co_auteurs(self, co_auteurs):
        """!
        @brief Mutateur pour les co-auteurs.
        @param co_auteurs Nouvelle liste de co-auteurs.
        """
        self.co_auteurs = co_auteurs

    def getType(self):
        """!
        @brief Surcharge pour retourner le type Arxiv.
        @return "Arxiv".
        """
        return self.type

    def __str__(self):
        """!
        @brief Surcharge de l'affichage.
        @return Description incluant le nombre de co-auteurs.
        """
        return super().__str__() + f" avec {len(self.co_auteurs)} co-auteurs"