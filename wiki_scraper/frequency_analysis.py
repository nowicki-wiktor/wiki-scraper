import math
import pandas as pd
import matplotlib.pyplot as plt
from wordfreq import top_n_list, word_frequency
from .word_counter import load_file

DEFAULT_LANGUAGE_CODE = "en"

def load_language_frequencies(language_code=DEFAULT_LANGUAGE_CODE, top_n=5000):
    words = top_n_list(language_code, top_n)
    frequencies = {}

    for w in words:
        w_low = w.lower()
        freq = word_frequency(w, language_code)
        if freq > 0.0:
            frequencies[w_low] = freq

    return frequencies

# tryb article 
def normalize_and_prep_table_article(article_frequencies, language_frequencies, how_many):
    article_series = pd.Series(article_frequencies, dtype=float)

    if article_series.empty:
        return pd.DataFrame(columns=["word", "frequency_in_article",
                                     "frequency_in_language"])
    sum_article = sum(article_frequencies.values())
    article_norm = article_series / sum_article
    article_sorted = article_norm.sort_values(ascending=False)

    article_top = article_sorted.iloc[:how_many]
    words = article_top.index

    language_series = pd.Series(language_frequencies, dtype=float)
    if not language_series.empty:
        language_for_words = language_series.reindex(words)
    else:
        language_for_words = pd.Series([math.nan] * len(words), index=words)

    df = pd.DataFrame({
        "word": words,
        "frequency_in_article": article_top.values,
        "frequency_in_language": language_for_words.values,
    })

    return df


def normalize_and_prep_table_language(article_frequencies, language_frequencies, how_many):
    language_series = pd.Series(language_frequencies, dtype=float)

    if language_series.empty:
        return pd.DataFrame(columns=["word", "frequency_in_article",
                                     "frequency_in_language"])

    language_sorted = language_series.sort_values(ascending=False)

    language_top = language_sorted.iloc[:how_many]
    words = language_top.index

    article_series = pd.Series(article_frequencies, dtype=float)
    if not article_series.empty:
        sum_article = sum(article_frequencies.values())
        article_norm = article_series / sum_article
        article_for_words = article_norm.reindex(words)
    else:
        article_for_words = pd.Series([math.nan] * len(words), index=words)

    df = pd.DataFrame({
        "word": words,
        "frequency_in_article": article_for_words.values,
        "frequency_in_language": language_top.values,
    })

    return df

def generate_chart(df, mode, os_path):
    if df.empty:
        print("Brak danych do wykresu.")
        return
    
    labels = df["word"].tolist()
    article_vals = df["frequency_in_article"].fillna(0.0).tolist()
    language_vals = df["frequency_in_language"].fillna(0.0).tolist()

    x = range(len(labels))
    width = 0.4

    plt.figure(figsize=(max(8, len(labels) * 0.6), 5))

    x_article = [i - width / 2 for i in x]
    x_language = [i + width / 2 for i in x]

    plt.bar(x_article, article_vals, width=width, label="article", color='blue')
    plt.bar(x_language, language_vals, width=width, label="language", color='red')

    plt.xticks(list(x), labels, rotation=45, ha="right")
    plt.ylabel("frequency")
    plt.title("frequency of some words on wiki (mode: {})".format(mode))
    plt.legend()
    plt.tight_layout()
    plt.savefig(os_path)
    plt.close()

    print("Wykres zapisano do pliku: {}".format(os_path))


def analyze_relative_word_frequency(mode, n, chart_path=None,
                                    language_code=DEFAULT_LANGUAGE_CODE):
    article_counts = load_file()
    if not article_counts:
        print("Plik word-counts.json jest pusty lub nie istnieje. "
              "Najpierw uruchom --count-words lub --auto-count-words.")
        return None

    # chcemy mieć przynajmniej 1000 słów języka,
    # ale także więcej niż n, żeby sortowanie miało sens
    top_n_language = max(1000, 2*n)
    language_freqs = load_language_frequencies(
        language_code=language_code,
        top_n=top_n_language,
    )

    if mode == "article":
        df = normalize_and_prep_table_article(article_counts, language_freqs, n)
    elif mode == "language":
        df = normalize_and_prep_table_language(article_counts, language_freqs, n)
    else:
        raise ValueError("Nieznany tryb: {}. Użyj 'article' lub 'language'.".format(mode))

    print(df)

    if chart_path is not None:
        generate_chart(df, mode, chart_path)

    return df
