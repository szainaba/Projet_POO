async def main():

    Bibli = bibli("C:/Users/utilisateur/Documents/Biblio")
    d = bibli_scrap("C:/Users/utilisateur/Documents/Biblio")
    await Bibli.alimenter("https://math.univ-angers.fr/~jaclin/biblio/livres/")
    await d.scrap("https://math.univ-angers.fr/~jaclin/biblio/livres/", profondeur=1, nbmax=100)
    Bibli.rapport_livres("PDF", r"C:\Users\utilisateur\Documents\Biblio\rapport_livres.pdf")
    Bibli.rapport_auteurs("PDF", r"C:\Users\utilisateur\Documents\Biblio\rapport_auteurs.pdf")
          
if __name__ == "__main__":
    asyncio.run(main())
