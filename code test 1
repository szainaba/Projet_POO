if __name__ == "__main__":
    # Création d'une instance de Bibli
    bibli = Bibli(r"C:\Users\utilisateur\Biblio")  #### lien pour windows pour recevoir les rapports

    # Création d'instances de LivreEPUB et LivrePDF
    livre_epub = LivreEPUB(r"C:\Users\utilisateur\Biblio\pdf.txt", "Titre EPUB", "Auteur EPUB", "Français", "Science Fiction", datetime(2022, 1, 1))
    livre_pdf = LivrePDF(r"C:\Users\utilisateur\Biblio\Ebook.txt", "Titre PDF", "Auteur PDF", "Anglais", "Informatique", datetime(2022, 2, 1))

    # Ajout des livres à la bibliothèque
    bibli.ajouter(livre_epub)
    bibli.ajouter(livre_pdf)

    # Génération de rapports
    bibli.rapport_livres("PDF", r"C:\Users\utilisateur\rapport_livres.txt")
    bibli.rapport_auteurs("EPUB", r"C:\Users\utilisateur\rapport_auteurs.txt")

    # Alimenter la bibliothèque depuis une URL
    bibli.alimenter("https://math.univ-angers.fr/~jaclin/biblio/livres/")

    # Vous pouvez maintenant accéder aux livres ajoutés à la bibliothèque
    for livre in bibli.livres:
        print(f"Titre: {livre.titre()}, Auteur: {livre.auteur()}, Type: {livre.type()}")
    Bibli2 = Bibli(r"C:\Users\utilisateur\Biblio")
    Bibli2.alimenter("https://math.univ-angers.fr/~jaclin/biblio/livres/")
    Bibli2.rapport_livres("PDF", r"C:\Users\utilisateur\rapport_livres.txt")
    Bibli2.rapport_auteurs("EPUB", r"C:\Users\utilisateur\rapport_auteurs.txt")

    # Exemple d'utilisation de BibliScrap
    d = BibliScrap()
    d.scrap("https://math.univ-angers.fr/~jaclin/biblio/livres/", profondeur=2, nbmax=5)
