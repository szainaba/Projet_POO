class EPUBLivre(BaseLivre):
    def __init__(self, titre, auteur, annee, lien):
        super().__init__(titre, auteur, annee, lien)
        # Charger des bibliothèques spécifiques à EPUB si nécessaire
    
    def lire_metadonnees(self):
        # Exemple d'implémentation pour lire les métadonnées d'un fichier EPUB
        print(f"Lecture des métadonnées pour l'EPUB '{self.titre}'")
        # Logique spécifique pour extraire les métadonnées de l'EPUB

    def afficher_contenu(self):
        # Exemple d'implémentation pour afficher le contenu d'un fichier EPUB
        print(f"Affichage du contenu pour l'EPUB '{self.titre}'")
        # Logique pour lire et afficher le contenu