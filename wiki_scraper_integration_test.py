import os

# sprawdza czy funkcjonalność --summary działa poprawnie
# porównuje oczekiwany początek tekstu z faktycznym.
# analogicznie koniec tekstu.
# korzysta z lokalnego pliku html


from wiki_scraper.article_scraper import ArticleScraper

def main():
    html_path = "data/team_rocket.html"

    if not os.path.exists(html_path):
        print("BŁĄD: Nie znaleziono pliku HTML:", html_path)
        return -1

    phrase = "Team Rocket"

    try:
        scraper = ArticleScraper(phrase=phrase, local_html_path=html_path)
        summary = scraper.summarise_article()
    except Exception as e:
        print(repr(e))
        return -1
    
    ok = True

    expected_beginning = "Team Rocket"
    expected_ending = "outpost in the Sevii Islands ."

    if not summary.startswith(expected_beginning):
        print("Tekst nie zaczyna się od " + expected_beginning)
        ok = False

    if not summary.endswith(expected_ending):
        print("Tekst nie kończy się na " + expected_ending)
        ok = False

    if not ok:
        return -1
    
    print("Funkcjonalność --summary działa poprawnie")

    return 0

if __name__ == "__main__":
    main()
    