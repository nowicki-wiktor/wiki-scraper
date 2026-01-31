import json
import os # do spawdzania istnienia pliku
import re # do ekstrakcji słów


WORD_COUNTS_PATH = "word-counts.json"

# zmienia wszystkie duze litery na małe i zwraca liste słów
def split_into_words(text):
    return re.findall(r"[A-Za-z]+", text.lower())

#zwraca słownik słowo -> liczba wystąpień
def count_words(text):
    words = split_into_words(text)
    quantity = {}
    for w in words:
        if w in quantity:
            quantity[w] += 1
        else:
            quantity[w] = 1
    return quantity

# zwraca aktualna zawartosc pliku WORD_COUNTS_PATH
def load_file(path=WORD_COUNTS_PATH):
    if not os.path.exists(path):
        return {}
    
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    result = {}
    for key, value in data.items():
        try:
            result[str(key)] = int(value)
        except (TypeError, ValueError):
            continue
    return result

# aktualizuje stary slownik o nowe wartości
def update_quantities(old_quantities, new_quantities):
    result = dict(old_quantities) # deep-kopia
    for word, quantity in new_quantities.items():
        if word in result:
            result[word] += quantity
        else:
            result[word] = quantity
    
    return result

#zapisuje słownik do pliku
def save_file_quantities(quantities, path=WORD_COUNTS_PATH):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(quantities, f, ensure_ascii=False, indent=2)
