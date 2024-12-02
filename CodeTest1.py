async def main():

    Bibli = bibli("C:/Users/utilisateur/Documents/Biblio")
    d = BibliScrap("C:/Users/utilisateur/Documents/Biblio")
    await Bibli.alimenter("https://math.univ-angers.fr/~jaclin/biblio/livres/")
    await d.scrap("https://math.univ-angers.fr/~jaclin/biblio/livres/", profondeur=1, nbmax=100)
    Bibli.rapport_livres("PDF", r"C:\Users\utilisateur\Documents\Biblio\rapport_livres.txt")
    Bibli.rapport_auteurs("PDF", r"C:\Users\utilisateur\Documents\Biblio\rapport_auteurs.txt")
          
if __name__ == "__main__":
    asyncio.run(main())
