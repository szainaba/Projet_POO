class LivrePDF(base_livre):
    def __init__(self, ressource, titre, auteur, langue, sujet, date_publication):
        super().__init__(ressource)
        self._titre = titre
        self._auteur = auteur
        self._langue = langue
        self._sujet = sujet
        self._date_publication = date_publication

    def type(self):
        return "PDF"

    def titre(self):
        return self._titre

    def auteur(self):
        return self._auteur

    def langue(self):
        return self._langue

    def sujet(self):
        return self._sujet

    def date(self):
        return self._date_publication