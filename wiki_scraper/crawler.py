import time # do opóźnień między ządaniami
from collections import deque # kolejka
from .article_scraper import ArticleScraper
from .config import BULBAPEDIA_BASE_URL
from .word_counter import *
from .utils import generate_url

class WikiCrawler:
    def __init__(self, start_phrase, max_depth, wait_seconds=0.0,
                 base_url=BULBAPEDIA_BASE_URL):
        self.start_phrase = start_phrase
        self.max_depth = max_depth
        self.wait_seconds = wait_seconds
        self.base_url = base_url
        self.visited = set()

    # BFS
    def crawl(self):
        global_quantities = load_file() # zawartość word-counts.json

        queue = deque()

        queue.append((self.start_phrase, 0))
        
        while queue:
            phrase, depth = queue.popleft()

            if phrase in self.visited:
                continue
            self.visited.add(phrase)

            print("{} ({})".format(phrase, generate_url(phrase)))

            scraper = ArticleScraper(phrase=phrase)

            try:
                text = scraper.get_article_text()
            except ValueError as e:
                print("Pominięto artykuł '{}': {}".format(phrase, e))
                continue

            new_quantities = count_words(text)
            global_quantities = update_quantities(global_quantities, new_quantities)

            if depth < self.max_depth:
                try:
                    links = scraper.get_links_to_articles()
                except Exception as e:
                    print("Błąd przy zbieraniu linków z '{}': {}".format(phrase, e))
                    links = []
                
                for link in links:
                    if link not in self.visited:
                        queue.append((link, depth + 1))

            if self.wait_seconds > 0 and queue:
                time.sleep(self.wait_seconds)

        save_file_quantities(global_quantities)
