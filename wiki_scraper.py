import argparse

from wiki_scraper.controller import ProgramController


def parse_args():
    parser = argparse.ArgumentParser(
        description="WikiScraper dla Bulbapedii"
    )

    parser.add_argument(
        "--summary",
        type=str,
    )

    parser.add_argument(
        "--count-words",
        dest="count_words",
        type=str,
    )

    parser.add_argument(
        "--table",
        type=str,
    )

    parser.add_argument(
        "--number",
        type=int,
    )

    parser.add_argument(
        "--first-row-is-header",
        dest="first_row_is_header",
        action="store_true",
    )

    parser.add_argument(
        "--auto-count-words",
        dest="auto_count_words",
        type=str,
    )

    parser.add_argument(
        "--depth",
        type=int,
    )

    parser.add_argument(
        "--wait",
        type=float,
        default=0.0,
    )

    parser.add_argument(
        "--analyze-relative-word-frequency",
        dest="analyze_relative_word_frequency",
        action="store_true",
    )

    parser.add_argument(
        "--mode",
        type=str,
        choices=["article", "language"],
    )

    parser.add_argument(
        "--count",
        type=int,
    )

    parser.add_argument(
        "--chart",
        type=str,
    )

    return parser.parse_args()


def main():
    args = parse_args()
    controller = ProgramController(args=args)
    controller.run()


if __name__ == "__main__":
    main()