import unittest

from wiki_scraper.word_counter import *

class TestWordCounter(unittest.TestCase):
    def test_split_into_words_basic(self):
        self.assertEqual(
            split_into_words("MIMUW is the best faculty in the World!"),
            ["mimuw", "is", "the", "best", "faculty", "in", "the", "world"]
        )
    
    def test_count_words(self):
        text = "Be or not to be"
        words = count_words(text)

        self.assertEqual(words["be"], 2)
        self.assertEqual(words["or"], 1)
        self.assertEqual(words["not"], 1)
        self.assertEqual(words["to"], 1)
        self.assertEqual(len(words), 4)

    def test_update_quantities(self):
        quantities_one = {"bee": 2, "cake": 7}
        quantities_two = {"cake": 3, "sunflower": 1}

        new_quantities = update_quantities(quantities_one, quantities_two)

        self.assertEqual(new_quantities,
                         {"bee": 2, "cake": 10, "sunflower": 1})