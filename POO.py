
import requests
import aiohttp
import asyncio
from bs4 import BeautifulSoup
from datetime import datetime
from ebooklib import epub
from PyPDF2 import PdfFileReader
from urllib.parse import urljoin
import warnings
import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
# importation du module UtlitaireFichier
from UtilitaireFichier import EpubFileInfo, PdfFileInfo

# Ignorer le UserWarning spécifique
warnings.filterwarnings("ignore", category=UserWarning)

class base_livre:

    def __init__(self,ressource):
        """
            ressource désigne soit le nom de fichier (local) correspondant au livre,
            soit une URL pointant vers un livre.
        """
        #raise NotImplementedError("à définir dans les sous-classes")

    def type(self):
        """ renvoie le type (EPUB, PDF, ou autre) du livre """
        raise NotImplementedError("à définir dans les sous-classes")

    def titre(self):
        """ renvoie le titre du livre """
        raise NotImplementedError("à définir dans les sous-classes")

    def auteur(self):
        """ renvoie l'auteur du livre """
        raise NotImplementedError("à définir dans les sous-classes")

    def langue(self):
        """ renvoie la langue du livre """
        raise NotImplementedError("à définir dans les sous-classes")

    def sujet(self):
        """ renvoie le sujet du livre """
        raise NotImplementedError("à définir dans les sous-classes")

    def date(self):
        """ renvoie la date de publication du livre """
        raise NotImplementedError("à définir dans les sous-classes")
##################################################################################

class base_bibli:
    def __init__(self,path):
        """ path désigne le répertoire contenant les livres de cette bibliothèque """
        #raise NotImplementedError("à définir dans les sous-classes")

    def ajouter(self,livre):
        """
        Ajoute le livre à la bibliothèque """
        raise NotImplementedError("à définir dans les sous-classes")

    def rapport_livres(self,format,fichier):
        """
            Génère un état des livres de la bibliothèque.
            Il contient la liste des livres,
            et pour chacun d'eux
            son titre, son auteur, son type (PDF ou EPUB), et le nom du fichier correspondant.

            format: format du rapport (PDF ou EPUB)
            fichier: nom du fichier généré
        """
        raise NotImplementedError("à définir dans les sous-classes")

    def rapport_auteurs(self,format,fichier):
        """
            Génère un état des auteurs des livres de la bibliothèque.
            Il contient pour chaque auteur
            le titre de ses livres en bibliothèque et le nom du fichier correspondant au livre.
            le type (PDF ou EPUB),
            et le nom du fichier correspondant.

            format: format du rapport (PDF ou EPUB)
            fichier: nom du fichier généré
        """
        raise NotImplementedError("à définir dans les sous-classes")

#livres sont au format EPUB et PDF dans un premier temps
#Créer les sous-classes EPUB_livre et PDF_livre

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

#creer classe PDF_livre
class PDF_livre(base_livre): 
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

    def ressource(self):
        """ renvoie la ressource du livre """
        return self.ressource 

    def type(self):
        """ renvoie le type (EPUB, PDF, ou autre) du livre """
        return "PDF"

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


class BibliScrap(simple_bibli):
    def __init__(self,path):

        super().__init__(path)
        self.downloaded_docs = 0
        self.session = requests.Session()
        self.livres = []

    async def scrap(self, url, profondeur, nbmax):
            self.nbmax = nbmax
            if profondeur <= 0 or self.downloaded_docs >= self.nbmax:
                return

            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(url) as response:
                        response.raise_for_status()
                        soup = BeautifulSoup(await response.text(), 'html.parser')
                        await self.download_documents(soup, url, session)

                        links = [urljoin(url, a['href']) for a in soup.find_all('a', href=True) if self.is_html_link(a)]
                        tasks = [self.scrap(link, profondeur - 1, self.nbmax) for link in links]
                        await asyncio.gather(*tasks)
            except (aiohttp.ClientError, aiohttp.InvalidURL, aiohttp.ClientResponseError) as e:
                print(f"Une erreur s'est produite lors du traitement de {url}: {str(e)}")


    def is_html_link(self, a_tag):
        # Vérifier si le lien pointe vers une page HTML (Content-Type)
        href = a_tag.get('href', '')
        try:
            response = self.session.head(href)
            content_type = response.headers.get('content-type', '').lower()
            return content_type.startswith('text/html')
        except requests.exceptions.RequestException:
            return False

    async def download_documents(self, soup, base_url, session):
            for link in soup.find_all('a', href=True):
                if self.downloaded_docs >= self.nbmax:
                    return

                href = link['href']
                if href.endswith('.pdf') or href.endswith('.epub'):
                    self.downloaded_docs += 1
                    self.livres.append(href)
                    file_name = href.split('/')[-1]
                    file_path = os.path.join(self._path, file_name)

                    async with session.get(urljoin(base_url, href)) as response:
                        if response.status == 200:
                            with open(file_path, 'wb') as file:
                                while True:
                                    chunk = await response.content.read(8192)
                                    if not chunk:
                                        break
                                    file.write(chunk)
                            print(f"Téléchargement réussi : {file_path}")
                        else:
                            print(f"Erreur lors du téléchargement de {href}")



async def main():

    Bibli = bibli("C:/Users/utilisateur/Documents/Biblio")
    d = BibliScrap("C:/Users/utilisateur/Documents/Biblio")
    await Bibli.alimenter("https://math.univ-angers.fr/~jaclin/biblio/livres/")
    await d.scrap("https://math.univ-angers.fr/~jaclin/biblio/livres/", profondeur=1, nbmax=100)
    Bibli.rapport_livres("PDF", r"C:\Users\utilisateur\Documents\Biblio\rapport_livres.txt")
    Bibli.rapport_auteurs("PDF", r"C:\Users\utilisateur\Documents\Biblio\rapport_auteurs.txt")
          
if __name__ == "__main__":
    asyncio.run(main())
