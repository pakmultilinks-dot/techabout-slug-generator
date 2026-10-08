"""Tests for slug_generator.py (12 tests)."""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(__file__))
from slug_generator import slugify, transliterate


class TestSlugGenerator(unittest.TestCase):
    def test_basic_title(self):
        self.assertEqual(slugify("Hello World"), "hello-world")

    def test_punctuation_removed(self):
        self.assertEqual(slugify("10 AI Trends to Watch in 2026!"),
                         "10-ai-trends-to-watch-in-2026")

    def test_multiple_separators_collapse(self):
        self.assertEqual(slugify("AI   ---   News:  What's   New?"),
                         "ai-news-what-s-new")

    def test_leading_trailing_junk_stripped(self):
        self.assertEqual(slugify("  ***Hello, World!!!  "), "hello-world")

    def test_underscores_become_hyphens(self):
        self.assertEqual(slugify("my_article_title"), "my-article-title")

    def test_unicode_transliterated(self):
        self.assertEqual(slugify("Café & Naïve Résumé"), "cafe-naive-resume")

    def test_numbers_kept(self):
        self.assertEqual(slugify("Top 5 Python Libraries 2026"), "top-5-python-libraries-2026")

    def test_empty_title_falls_back(self):
        self.assertEqual(slugify(""), "untitled")
        self.assertEqual(slugify("!!!"), "untitled")
        self.assertEqual(slugify(None), "untitled")

    def test_custom_fallback(self):
        self.assertEqual(slugify("", fallback="no-title"), "no-title")

    def test_max_length_cuts_at_word_boundary(self):
        slug = slugify("The quick brown fox jumps over the lazy dog", max_length=20)
        self.assertTrue(len(slug) <= 20)
        self.assertEqual(slug, "the-quick-brown-fox")

    def test_max_length_no_hyphen_inside(self):
        slug = slugify("Supercalifragilistic", max_length=10)
        self.assertEqual(slug, "supercalif")

    def test_max_length_zero_means_no_limit(self):
        title = "a " * 100
        self.assertGreater(len(slugify(title.strip())), 100)

    def test_already_clean_slug_unchanged(self):
        self.assertEqual(slugify("already-clean-slug"), "already-clean-slug")

    def test_transliterate_helper(self):
        self.assertEqual(transliterate("Straße"), "Strae")


if __name__ == "__main__":
    unittest.main(verbosity=2)
