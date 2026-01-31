# wiki_scraper/table_grabber.py

import pandas as pd

# Znajdź n-tą tabelę <table> w głównej części artykułu (div.mw-parser-output).
# Numeracja od 1.
def get_nth_table_using_soup(soup, table_number):
    content_div = soup.find("div", class_="mw-parser-output")
    if content_div is None:
        raise RuntimeError(
            "Nie udało się znaleźć głównego kontenera treści artykułu "
        )

    tables = content_div.find_all("table")
    if not tables:
        raise ValueError("Na stronie nie znaleziono żadnych tabel.")

    if table_number < 1 or table_number > len(tables):
        raise ValueError(
            "Poproszono o tabelę numer {}, ale na stronie jest tylko {} tabel."
            .format(table_number, len(tables))
        )

    return tables[table_number - 1]


def table_to_dataframe(table_tag, first_row_is_header=False):
    rows = []

    # zbierz wszystkie wiersze z tabeli
    for tr in table_tag.find_all("tr"):
        cells = tr.find_all(["th", "td"])
        row_texts = [cell.get_text(" ", strip=True) for cell in cells]
        if row_texts:
            rows.append(row_texts)

    if not rows:
        return pd.DataFrame()

    # maksymalna długość wiersza – typowy wiersz danych
    max_len = max(len(r) for r in rows)

    if first_row_is_header:
        # znajdź pierwszy wiersz, który ma max_len komórek – uznajemy go za nagłówek
        header_idx = 0
        for i, r in enumerate(rows):
            if len(r) == max_len:
                header_idx = i
                break

        header_row = rows[header_idx]
        data_rows_raw = rows[header_idx + 1:]

        n_cols = len(header_row)

        # zakładamy: pierwsza kolumna = nagłówki wierszy, reszta = dane
        column_names = header_row[1:]
        data_rows = []
        row_index = []

        for r in data_rows_raw:
            if not r:
                continue
            # dopasuj długość do nagłówka (przytnij lub dopadnij pustymi)
            r = (r + [""] * n_cols)[:n_cols]

            row_index.append(r[0])
            data_rows.append(r[1:])

        df = pd.DataFrame(data_rows, index=row_index, columns=column_names)
    else:
        # brak nagłówków kolumn – generujemy je automatycznie
        data_rows = []
        row_index = []

        for r in rows:
            if not r:
                continue
            # dopasuj długość do max_len
            r = (r + [""] * max_len)[:max_len]
            row_index.append(r[0])
            data_rows.append(r[1:])

        df = pd.DataFrame(data_rows, index=row_index)

    return df

# Policz, ile razy każda wartość pojawia się w DataFrame (bez nagłówków).
# Zwraca pandas.Series (wartość -> liczba wystąpień).
def count_table_values(df):
    if df.empty:
        return pd.Series(dtype=int)

    values = df.values.ravel()

    cleaned = [
        v for v in values
        if isinstance(v, str) and v.strip() != ""
    ]

    if not cleaned:
        return pd.Series(dtype=int)

    s = pd.Series(cleaned)
    return s.value_counts()