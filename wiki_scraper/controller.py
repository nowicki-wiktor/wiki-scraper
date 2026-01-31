from .article_scraper import ArticleScraper
from .utils import *
from .word_counter import *
from .table_grabber import *
from .crawler import WikiCrawler
from .frequency_analysis import analyze_relative_word_frequency

class ProgramController:
    def __init__(self, args):
        self.args = args

    def run(self):
        if self.args.summary is not None:
            self.handle_summary(self.args.summary)
        elif self.args.count_words is not None:
            self.handle_count_words(self.args.count_words)
        elif self.args.table is not None:
            if self.args.number is None:
                raise SystemExit(
                    "Przy użyciu --table musisz też podać --number n "
                    "(numer tabeli na stronie, licząc od 1)."
                )
            self.handle_table(
                phrase=self.args.table,
                table_number=self.args.number,
                first_row_is_header=self.args.first_row_is_header,
            )
        elif self.args.analyze_relative_word_frequency:
            if self.args.mode not in ("article", "language"):
                raise SystemExit(
                    "Przy --analyze-relative-word-frequency musisz podać "
                    "--mode article lub --mode language."
                )
            if self.args.count is None:
                raise SystemExit(
                    "Przy --analyze-relative-word-frequency musisz podać --count n."
                )
            self.handle_analyze_relative_word_frequency(
                mode=self.args.mode,
                n=self.args.count,
                chart_path=self.args.chart,
            )
        elif self.args.auto_count_words is not None:
            if self.args.depth is None:
                raise SystemExit(
                    "Przy użyciu --auto-count-words musisz też podać --depth n."
                )
            wait = self.args.wait if self.args.wait is not None else 0.0
            self.handle_auto_count_words(
                start_phrase=self.args.auto_count_words,
                depth=self.args.depth,
                wait_seconds=wait,
            )
        else:
            raise SystemExit(
                "Nie podano żadnego polecenia."
            )

    def handle_summary(self, phrase):
        """
        Obsługa polecenia --summary "fraza"
        """
        scraper = ArticleScraper(phrase=phrase)

        try:
            summary = scraper.summarise_article()
        except ValueError as exc:
            print(str(exc))
            return

        print(summary)
        print("Wyjście programu na licencji BY-NC-SA " \
            "stworzone na podstawie artykułu dostępnego na stronie: {}"
            .format(generate_url(phrase)))

    def handle_count_words(self, phrase):
        """
        Obsługa polecenia --count-words.

        - pobiera pełny tekst artykułu,
        - liczy słowa,
        - aktualizuje plik word-counts.json.
        """
        scraper = ArticleScraper(phrase=phrase)

        try:
            article_text = scraper.get_article_text()
        except ValueError as exc:
            print(str(exc))
            return

        new_quantities= count_words(article_text)

        old_quantities = load_file()

        updated_quantities = update_quantities(old_quantities, new_quantities)

        save_file_quantities(updated_quantities)

        print("Wyjście programu na licencji BY-NC-SA " \
            "stworzone na podstawie artykułu dostępnego na stronie: {}"
            .format(generate_url(phrase)))


    def handle_table(self, phrase, table_number, first_row_is_header):
        """
        Obsługa polecenia --table "fraza" --number n [--first-row-is-header].

        - pobiera stronę dla frazy,
        - znajduje n-tą tabelę,
        - zapisuje ją do CSV,
        - wypisuje tabelę,
        - wypisuje statystykę: ile razy dana wartość wystąpiła (bez nagłówków).
        """
        scraper = ArticleScraper(phrase=phrase)

        try:
            soup = scraper.get_soup()
        except ValueError as exc:
            print(str(exc))
            return

        try:
            table_t = get_nth_table_using_soup(soup, table_number)
        except (RuntimeError, ValueError) as exc:
            print(str(exc))
            return

        df = table_to_dataframe(table_t, first_row_is_header=first_row_is_header)

        # nazwa pliku CSV: fraza z podkreślnikami + .csv
        filename = "{}.csv".format(replace_space_with_underscore(phrase))

        # zapisujemy tabelę do pliku CSV
        df.to_csv(filename, index=True)

        print(df)

        # policz częstości wartości w tabeli (bez nagłówków)
        value_counts = count_table_values(df)

        if value_counts.empty:
            print("\nTabela nie zawiera żadnych tekstowych wartości do zliczenia.")
        else:
            print("\nLiczba wystąpień każdej wartości w tabeli:")
            print(value_counts.to_frame(name="liczność"))
        
        print("Wyjście programu na licencji BY-NC-SA " \
            "stworzone na podstawie artykułu dostępnego na stronie: {}"
            .format(generate_url(phrase)))

    def handle_auto_count_words(self, start_phrase, depth, wait_seconds):
        crawler = WikiCrawler(
            start_phrase=start_phrase,
            max_depth=depth,
            wait_seconds=wait_seconds,
        )
        print("Wyjście programu na licencji BY-NC-SA " \
            "stworzone na podstawie artykułów dostępnych na stronach: ")
        crawler.crawl()
        print(
            "Zakończono auto-count-words od frazy '{}' do głębokości {}."
            .format(start_phrase, depth)
        )

    def handle_analyze_relative_word_frequency(self, mode, n, chart_path):
        """
        Obsługa polecenia:
        --analyze-relative-word-frequency --mode TRYB --count n [--chart plik.png]
        """
        analyze_relative_word_frequency(
            mode=mode,
            n=n,
            chart_path=chart_path,
            language_code="en",
        )