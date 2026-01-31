import unittest

from wiki_scraper.utils import *

class TestUtils(unittest.TestCase):
    def test_replace_text_with_underscore(self):
        self.assertEqual(replace_space_with_underscore("     Team Rocket "), "Team_Rocket")

    def test_is_this_href_wrong(self):
        self.assertFalse(is_wiki_article_href("/wiki/File:Bulbasaur.png"))

    def test_href_to_phrase(self):
        self.assertEqual(href_to_phrase("/wiki/Team_Rocket"), "Team Rocket")

    