from .config import BULBAPEDIA_BASE_URL
from .utils import *

import requests # do pobierania stron
from bs4 import BeautifulSoup # do operacji na pobranych stronach HTML

class ArticleScraper:
    def __init__(self, phrase, local_html_path=None):
        self.phrase = phrase
        self.local_html_path = local_html_path
        self._html = None # bufor do pobranego html
        self._soup = None # bufor do obiektu BS

    # pobiera stronę z pliku/internetu uzywając requests
    def scrape_html(self):
        if self._html is not None:
            return self._html
        
        if self.local_html_path is not None:
            with open(self.local_html_path, "r", encoding="utf-8") as f:
                self._html = f.read()
            return self._html

        # pobieramy z internetu
        url = generate_url(self.phrase)
        website = requests.get(url)

        # sprawdzenie błędów
        # nie ma artykułu pod tym URL
        if website.status_code == 404:
            raise ValueError(
                "Artykuł dla frazy '{}' nie został znaleziony pod adresem: {}"
                .format(self.phrase, url)
            )
        # pozostałe błędy
        website.raise_for_status()

        self._html = website.text
        return self._html

    # tworzy obiekt BeautifulSoup dla strony _html z parserem html
    def get_soup(self):
            if self._soup is not None:
                return self._soup
            
            html = self.scrape_html()
            self._soup = BeautifulSoup(html, "html.parser")
            return self._soup
    
    # zwraca pierwszy fragment z <div> w html
    def _get_content_div(self):
        soup = self.get_soup()
        content_div = soup.find("div", class_="mw-parser-output")
        if content_div is None:
            raise RuntimeError(
                "Nie udało się znaleźć głównego kontenera treści artykułu "
                "(div.mw-parser-output)."
            )
        return content_div
    
    # zwraca pierwszy paragraf ze strony
    def summarise_article(self):
        content_div = self._get_content_div()
        first_p = content_div.find("p")
        if first_p is None:
            raise RuntimeError("Nie udało się znaleźć pierwszego paragrafu")
        
        return first_p.get_text(separator=" ", strip=True)
    
    # zwroc cały tekst artykułu 
    def get_article_text(self):
        content_div = self._get_content_div()
        return content_div.get_text(separator=" ", strip=True)
    
    # pobiera wszystkie tagi <a>, wyciąga href
    # a następnie konwertuje je na frazy wyszukiwań
    # i zwraca listę tychze fraz
    def get_links_to_articles(self):
        content_div = self._get_content_div()
        link_tags = content_div.find_all("a", href=True)

        phrases = []
        seen = set()

        for tag in link_tags:
            href = tag["href"]
            phrase = href_to_phrase(href)
            if phrase and phrase not in seen:
                seen.add(phrase)
                phrases.append(phrase)

        return phrases