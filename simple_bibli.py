import os
from base_bibli import base_bibli

#Créer une sous-classe simple_bibli de base_bibli , et l’alimenter avec quelques livres matérialisés sous forme de chiers situés en local.

class simple_bibli(base_bibli):
    """
    Classe représentant une bibliothèque simple.
    Hérite de la classe base_bibli.
    """

    def __init__(self,path):
        """ 
        Initialise une instance de la classe simple_bibli.
        
        Args:
            path (str): Le répertoire contenant les livres de cette bibliothèque.
        """
        super().__init__(path)
        self._path = path
        self._livres = []

    def ajouter(self,livre):
        """
        Ajoute un livre à la bibliothèque.
        
        Args:
            livre (Livre): Le livre à ajouter.
        """
        self._livres.append(livre)


    def rapport_auteurs(self, format, fichier):
        """
        Génère un état des auteurs des livres de la bibliothèque au format PDF.
        
        Args:
            format (str): Le format du rapport (PDF ou EPUB).
            fichier (str): Le nom du fichier généré.
        """
        if format != 'PDF':
            print("Le format spécifié n'est pas pris en charge pour ce rapport.")
            return

        # Dimensions de la page
        largeur, hauteur = letter

        # Création du document PDF
        c = canvas.Canvas(fichier, pagesize=letter)

        # Marge basse pour la nouvelle page
        marge_basse = 50

        # Position verticale initiale
        y_offset = hauteur - 50

        c.drawString(100, y_offset, "Liste des auteurs de la bibliothèque :")
        y_offset -= 20  # Retour à la ligne après le titre initial

        for livre in self._livres:
            if y_offset < marge_basse:
                # Nouvelle page si l'espace est insuffisant
                c.showPage()
                c.drawString(100, hauteur - 50, "Liste des auteurs de la bibliothèque :")
                y_offset = hauteur - 70  # Réinitialisation de la position verticale

            c.drawString(100, y_offset, f"Auteur : {livre.auteur()}")
            y_offset -= 20  # Retour à la ligne après l'écriture de l'auteur

            c.drawString(100, y_offset, f"Titre : {livre.titre()}")
            y_offset -= 20  # Retour à la ligne après l'écriture du titre

            c.drawString(100, y_offset, f"Type : {livre.type()}")
            y_offset -= 20  # Retour à la ligne après l'écriture du type

            c.drawString(100, y_offset, f"Nom du fichier : {livre.ressource}")
            y_offset -= 40  # Retour à la ligne plus grand après l'écriture du nom du fichier

        c.save()
        print(f"Le rapport des auteurs a été généré au format PDF : {fichier}")

    def rapport_livres(self, format, fichier):
        """
        Génère un état  des livres de la bibliothèque au format PDF.
        
        Args:
            format (str): Le format du rapport (PDF ou EPUB).
            fichier (str): Le nom du fichier généré.
        """
        if format != 'PDF':
            print("Le format spécifié n'est pas pris en charge pour ce rapport.")
            return

        # Dimensions de la page
        largeur, hauteur = letter

        # Création du document PDF
        c = canvas.Canvas(fichier, pagesize=letter)

        # Marge basse pour la nouvelle page
        marge_basse = 50

        # Position verticale initiale
        y_offset = hauteur - 50

        c.drawString(100, y_offset, "Liste des livres de la bibliothèque :")
        y_offset -= 20  # Retour à la ligne après le titre initial

        for livre in self._livres:
            if y_offset < marge_basse:
                # Nouvelle page si l'espace est insuffisant
                c.showPage()
                c.drawString(100, hauteur - 50, "Liste des livres de la bibliothèque :")
                y_offset = hauteur - 70  # Réinitialisation de la position verticale

            c.drawString(100, y_offset, f"Auteur : {livre.auteur()}")
            y_offset -= 20  # Retour à la ligne après l'écriture de l'auteur

            c.drawString(100, y_offset, f"Titre : {livre.titre()}")
            y_offset -= 20  # Retour à la ligne après l'écriture du titre

            c.drawString(100, y_offset, f"Type : {livre.type()}")
            y_offset -= 20  # Retour à la ligne après l'écriture du type

            c.drawString(100, y_offset, f"Nom du fichier : {livre.ressource}")
            y_offset -= 40  # Retour à la ligne plus grand après l'écriture du nom du fichier

        c.save()
        print(f"Le rapport des livres a été généré au format PDF : {fichier}")
