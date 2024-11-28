class simple_bibli(base_bibli):
    def __init__(self, path):
        self.path = path
        self.livres = []

    def ajouter(self, livre):
        # Ajoute le livre à la bibliothèque
        self.livres.append(livre)

    def rapport_livres(self, format, fichier):
        # Génère un rapport sur les livres de la bibliothèque
        with open(fichier, 'w') as rapport:
            rapport.write(f"Liste des livres de la bibliothèque au format :\n")
            for livre in self.livres:
                rapport.write(f"Titre: {livre.titre()}, Auteur: {livre.auteur()}, Type: {livre.type()}, Fichier: {livre.ressource}\n")

    def rapport_auteurs(self, format, fichier):
        # Génère un rapport sur les auteurs des livres de la bibliothèque
        auteurs = {}
        with open(fichier, 'w') as rapport:
            rapport.write(f"Liste des auteurs des livres de la bibliothèque :\n")
            for livre in self.livres:
                auteur = livre.auteur()
                if auteur not in auteurs:
                    auteurs[auteur] = []
                auteurs[auteur].append(f"Titre: {livre.titre()}, Type: {livre.type()}, Fichier: {livre.ressource}\n")
            
            for auteur, livres in auteurs.items():
                rapport.write(f"Auteur: {auteur}\n")
                rapport.write("".join(livres))
