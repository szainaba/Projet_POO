import numpy as np
import os
import requests
from datetime import datetime
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from urllib.request import urlretrieve
import simple_bibli
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

