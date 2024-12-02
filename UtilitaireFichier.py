from datetime import datetime
from io import BytesIO
from PyPDF2 import PdfReader
from ebooklib import epub
import aiohttp
import asyncio
import tempfile
import warnings
import os

# Ignorer le UserWarning spécifique
warnings.filterwarnings("ignore", category=UserWarning)

class FileInfo:
    def __init__(self, title='Titre inconnu', subject='Sujet inconnu', language='Langue inconnue', author='Auteur inconnu', date='Date inconnue',ressource='Ressource inconnue'):
        self.title = title
        self.subject = subject
        self.language = language
        self.author = author
        self.date = date
        self.ressource = ressource
        

class EpubFileInfo(FileInfo):
    async def extract_metadata(self, url):
        try:
            async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        temp_file = tempfile.NamedTemporaryFile(delete=True)
                        temp_file.write(await response.read())
                        temp_file.seek(0)

                        book = epub.read_epub(temp_file.name)
                        self.title = book.get_metadata('DC', 'title')[0][0] if book.get_metadata('DC', 'title') else 'Titre inconnu'
                        self.author = book.get_metadata('DC', 'creator')[0][0] if book.get_metadata('DC', 'creator') else 'Auteur inconnu'
                        self.language = book.get_metadata('DC', 'language')[0][0] if book.get_metadata('DC', 'language') else 'Langue inconnue'
                        self.subject = book.get_metadata('DC', 'subject')[0][0] if book.get_metadata('DC', 'subject') else 'Sujet inconnu'
                        self.date = book.get_metadata('DC', 'date')[0][0] if book.get_metadata('DC', 'date') else 'Date inconnue'
                        self.ressource = os.path.basename(url)
                        return self
                    else:
                        pass
                        #print(f"Erreur lors de la récupération du contenu pour {url}")
        except Exception as e:
            #print(f"Une erreur s'est produite : {e}")
            return None

class PdfFileInfo(FileInfo):

    async def extract_metadata(self, url):
        try:
            async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        pdf_data = await response.read()
                        pdf = PdfReader(BytesIO(pdf_data))

                        metadata = pdf.metadata
                        
                        self.title = metadata.get('/Title', 'Titre inconnu')
                        self.subject = metadata.get('/Subject', 'Sujet inconnu')
                        self.language = metadata.get('/Language', 'Langue inconnue')
                        self.author = metadata.get('/Author', 'Auteur inconnu')
                        self.ressource = os.path.basename(url)
                        #date = metadata.get('/CreationDate', 'Date inconnue')
                        #date = datetime.strptime(date[2:10], '%Y%m%d')
                        self.date = "Date inconnue"

                        return self
                    else:
                        pass
                        #print(f"Erreur lors de la récupération du contenu pour {url}")
        except Exception as e:
            #print(f"Une erreur s'est produite : {e}")
            return None


