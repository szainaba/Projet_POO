import numpy as np
import os
import requests
from datetime import datetime
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from urllib.request import urlretrieve
class BibliScrap:
    def __init__(self):
        self.downloaded_docs = 0
        self.session = requests.Session()
        self.livres = []

    def scrap(self, url, profondeur, nbmax):
        # Vérifier les conditions d'arrêt
        self.nbmax = nbmax
        if profondeur <= 0 or self.downloaded_docs >= self.nbmax :
            return

        try:
            # Télécharger la page web
            response = self.session.get(url,verify=False)
            response.raise_for_status()  # Gérer les erreurs HTTP

            soup = BeautifulSoup(response.text, 'html.parser')

            # Télécharger les documents PDF et EPUB
            self.download_documents(soup,url)

            # Extraire les liens vers d'autres pages web HTML
            links = [urljoin(url, a['href']) for a in soup.find_all('a', href=True) if self.is_html_link(a)]

            # Réitérer le processus pour chaque lien
            for link in links:
                self.scrap(link, profondeur - 1, self.nbmax)
        except requests.exceptions.RequestException as e:
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

    def download_documents(self, soup,url):
        # Télécharger les documents PDF et EPUB
        response = self.session.get(url)
        response.raise_for_status()
        for link in soup.find_all('a', href=True):
            if self.downloaded_docs >= self.nbmax:
                return

            href = link['href']
            if href.endswith('.pdf') or href.endswith('.epub'):
                self.downloaded_docs += 1
                file_name = f"downloaded_file_{self.downloaded_docs}.{href.split('.')[-1]}"
                urlretrieve(urljoin(url,href), file_name)
                print(f"Téléchargement réussi : {file_name}")