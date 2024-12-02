from base_livre import *
class EPUB_livre(base_livre): 
    def __init__(self, ressource, titre, auteur, langue, sujet, date_publication):
        """
            ressource désigne soit le nom de fichier (local) correspondant au livre,
            soit une URL pointant vers un livre.
        """
        super().__init__(ressource)
        self._titre = titre
        self._auteur = auteur
        self._langue = langue
        self._sujet = sujet
        self._date_publication = date_publication
        self.ressource = ressource

    def type(self):
        """ renvoie le type (EPUB, PDF, ou autre) du livre """
        return "EPUB"

    def titre(self):
        """ renvoie le titre du livre """
        return self._titre

    def auteur(self):
        """ renvoie l'auteur du livre """
        return self._auteur

    def langue(self):
        """ renvoie la langue du livre """
        return self._langue

    def sujet(self):
        """ renvoie le sujet du livre """
        return self._sujet

    def date(self):
        """ renvoie la date de publication du livre """
        return self._date_publication

    def ressource(self):
        """ renvoie la ressource du livre """
        return self.ressource
