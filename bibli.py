import requests
from bs4 import BeautifulSoup
import os
from simple_bibli import simple_bibli
class bibli(simple_bibli):
    def __init__(self, path):
        super().__init__(path)
        self.livres = []
    def ajouter(self, livre):
        self.livres.append(livre)

    def alimenter(self,url):
        page = requests.get("https://math.univ-angers.fr/~jaclin/biblio/livres/", verify=False)
        titre = []
        if page.status_code == 200:
            soup = BeautifulSoup(page.content, 'lxml')
            balises_livres = soup.find_all('tr')
            for balise_livre in balises_livres:
               link = balise_livre.a
               if link is not None:
                    titre.append(link["href"])
                    if link["href"].endswith("pdf"):
                        livre = LivrePDF(url+link["href"],link["href"], "unknown", "unknown", "unknown", datetime(2022, 1, 1))
                        self.ajouter(livre)
                    elif link["href"].endswith("epub"):
                        livre = LivreEPUB(url+link["href"],link["href"], "unknown", "unknown", "unknown", datetime(2022, 1, 1))
                        self.ajouter(livre)
