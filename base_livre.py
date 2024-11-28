import numpy as np
import os
import requests
from datetime import datetime
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from urllib.request import urlretrieve

class base_livre:
  def __init__(self,ressource):
    self.ressource = ressource

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
