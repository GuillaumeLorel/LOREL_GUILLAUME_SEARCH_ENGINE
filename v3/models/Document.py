"""!
# Document.py

Module contenant les classes représentant les documents (Mère et Filles).

**Author:** LOREL Guillaume  
**Version:** 1.0
"""

class Document:
    """!
    # Document

    Classe mère représentant un document générique.
    """

    def __init__(self, titre, auteur, date, url, texte):
        """!
        Constructeur de la classe Document.

        **Parameters**
        - **titre**: Titre du document.
        - **auteur**: Auteur du document.
        - **date**: Date de publication (format ISO).
        - **url**: Lien vers le document.
        - **texte**: Contenu textuel du document.
        """
        self.titre = titre
        self.auteur = auteur
        self.date = date
        self.url = url
        self.texte = texte
        self.type = "Inconnu"

    def get_titre(self):
        """!
        Accesseur pour le titre.

        **Returns**
        - Le titre du document.
        """
        return self.titre

    def get_auteur(self):
        """!
        Accesseur pour l'auteur.

        **Returns**
        - L'auteur du document.
        """
        return self.auteur

    def get_date(self):
        """!
        Accesseur pour la date.

        **Returns**
        - La date de publication du document.
        """
        return self.date

    def get_url(self):
        """!
        Accesseur pour l'URL.

        **Returns**
        - L'URL du document.
        """
        return self.url

    def get_texte(self):
        """!
        Accesseur pour le texte.

        **Returns**
        - Le contenu textuel du document.
        """
        return self.texte

    def getType(self):
        """!
        Accesseur pour le type de document.

        **Returns**
        - Le type sous forme de chaîne de caractères.
        """
        return self.type

    def __str__(self):
        """!
        Représentation textuelle du document.

        **Returns**
        - Chaîne décrivant le document (titre).
        """
        return f"Titre du document: {self.titre}"

    def afficher_informations(self):
        """!
        Affiche toutes les informations du document dans la console.
        """
        print(f"Titre: {self.titre}")
        print(f"Auteur: {self.auteur}")
        print(f"Date: {self.date}")
        print(f"URL: {self.url}")
        print(f"Texte: {self.texte}")
    

class RedditDocument(Document):
    """!
    # RedditDocument

    Classe fille représentant un post Reddit.

    See: Document
    """
    def __init__(self, titre, auteur, date, url, texte, nb_comments):
        """!
        Constructeur de RedditDocument.

        **Parameters**
        - **titre**: Titre du post.
        - **auteur**: Auteur du post.
        - **date**: Date de publication (ISO).
        - **url**: Lien vers le post.
        - **texte**: Contenu du post.
        - **nb_comments**: Nombre de commentaires du post.
        """
        super().__init__(titre=titre, auteur=auteur, date=date, url=url, texte=texte)
        self.nb_comments = nb_comments
        self.type = "Reddit"

    def get_nb_comments(self):
        """!
        Accesseur pour le nombre de commentaires.

        **Returns**
        - Nombre de commentaires (int).
        """
        return self.nb_comments

    def getType(self):
        """!
        Surcharge pour retourner le type Reddit.

        **Returns**
        - "Reddit".
        """
        return self.type

    def __str__(self):
        """!
        Surcharge de l'affichage.

        **Returns**
        - Description incluant le nombre de commentaires.
        """
        return super().__str__() + f" avec {self.nb_comments} commentaires"
        

class ArxivDocument(Document):
    """!
    # ArxivDocument

    Classe fille représentant un article Arxiv.

    See: Document
    """
    def __init__(self, titre, auteur, date, url, texte, co_auteurs=None):
        """!
        Constructeur d'ArxivDocument.

        **Parameters**
        - **titre**: Titre de l'article.
        - **auteur**: Auteur principal.
        - **date**: Date de publication (ISO).
        - **url**: Lien vers l'entrée Arxiv.
        - **texte**: Résumé / contenu textuel.
        - **co_auteurs**: Liste des co-auteurs (optionnel).
        """
        super().__init__(titre=titre, auteur=auteur, date=date, url=url, texte=texte)
        self.co_auteurs = co_auteurs if co_auteurs is not None else []
        self.type = "Arxiv"

    def get_co_auteurs(self):
        """!
        Accesseur pour les co-auteurs.

        **Returns**
        - Liste des co-auteurs.
        """
        return self.co_auteurs
    
    def set_co_auteurs(self, co_auteurs):
        """!
        Mutateur pour les co-auteurs.

        **Parameters**
        - **co_auteurs**: Nouvelle liste de co-auteurs.
        """
        self.co_auteurs = co_auteurs

    def getType(self):
        """!
        Surcharge pour retourner le type Arxiv.

        **Returns**
        - "Arxiv".
        """
        return self.type

    def __str__(self):
        """!
        Surcharge de l'affichage.

        **Returns**
        - Description incluant le nombre de co-auteurs.
        """
        return super().__str__() + f" avec {len(self.co_auteurs)} co-auteurs"