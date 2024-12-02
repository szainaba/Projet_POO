import requests
from bs4 import BeautifulSoup
import os
from simple_bibli import simple_bibli
from LivreEPUB import *
from LivrePDF import *
class bibli(simple_bibli):
    def __init__(self,path):
        """ path désigne le répertoire contenant les livres de cette bibliothèque """
        super().__init__(path)
        self._path = path
        self._livres = []

    def ajouter(self, livre):
        self._livres.append(livre)

    async def alimenter(self,url):
        page = requests.get(url, verify=False)


        if page.status_code == 200:
            soup = BeautifulSoup(page.content, 'lxml')

        # Liste pour stocker les valeurs de href
        href_list = []

        # Parcourir toutes les balises 'tr'
        for tr_tag in soup.find_all('tr'):
            # Trouver la balise 'a' à l'intérieur de chaque balise 'tr'
            a_tag = tr_tag.find('a')
            if a_tag and 'href' in a_tag.attrs:
                # Ajouter la valeur de 'href' à la liste
                href_list.append(url+a_tag['href'])

        #creer une liste de lien pour les livres en pdf et epub
        liste_pdf = []
        liste_epub = []



        # Parcourir la liste des liens
        for link in href_list:
            # Vérifier si le lien se termine par 'pdf'
            if link.endswith('pdf'):
                liste_pdf.append(link)
            # Vérifier si le lien se termine par 'epub'
            elif link.endswith('epub'):
                liste_epub.append(link)
        
        print("Début de l'alimentation de la bibliothèque")
        print("\n  Téléchargement des livres en cours...")

        tasks = []

        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
            for url in liste_pdf:
                file_info = PdfFileInfo()
                task = asyncio.create_task(file_info.extract_metadata(url))
                tasks.append(task)
            # Attendre que toutes les tâches soient terminées
            results = await asyncio.gather(*tasks)
            # Créer des objets livre avec les métadonnées extraites
            for info in results:
                if info:
                    livre= PDF_livre(info.ressource, info.title, info.author, info.language, info.subject, info.date)
                    self.ajouter(livre)

        tasks = []
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
            for url in liste_epub:
                file_info = EpubFileInfo()
                task = asyncio.create_task(file_info.extract_metadata(url))
                tasks.append(task)
            # Attendre que toutes les tâches soient terminées
            results = await asyncio.gather(*tasks)
            # Créer des objets livre avec les métadonnées extraites
            for info in results:
                if info:
                    livre= EPUB_livre(info.ressource, info.title, info.author, info.language, info.subject, info.date)
                    self.ajouter(livre)

            print("Fin de l'alimentation de la bibliothèque")        

