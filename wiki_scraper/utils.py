from .config import BULBAPEDIA_BASE_URL

# Usuwa białe znaki z początku i końca ciągu oraz zamienia
# wszystkie spacje na podkreślenia
def replace_space_with_underscore(text):
    if not text or not isinstance(text, str):
        return None
    return text.strip().replace(" ", "_")

# Wywołuje replace_space_with_underscore,
# dokleja wynik do BULBAPEDIA_BASE_URL
# i zwraca pełny URL artykułu wiki
def generate_url(text):
    return BULBAPEDIA_BASE_URL + replace_space_with_underscore(text)

# Sprawdza czy href jest poprawnym linkiem
# do artykułu
def is_wiki_article_href(href):
    if not href or not isinstance(href, str):
        return False

    if not href.startswith("/wiki/"):
        return False

    rest = href[len("/wiki/"):] #usuwa prefiks /wiki/ z początku href
    rest = rest.split("#", 1)[0]
    rest = rest.split("?", 1)[0]

    if not rest:
        return False

    if ":" in rest:
        return False
    
    return True

# zamienia link (href) na frazę wyszukiwana
def href_to_phrase(href):
    if not is_wiki_article_href(href):
        return None

    rest = href[len("/wiki/"):]
    rest = rest.split("#", 1)[0]
    rest = rest.split("?", 1)[0]

    if not rest:
        return None

    slug = rest
    phrase = slug.replace("_", " ")
    return phrase