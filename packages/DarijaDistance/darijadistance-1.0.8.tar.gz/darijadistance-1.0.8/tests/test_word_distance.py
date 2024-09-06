# python -m unittest discover -s tests
import unittest
from DarijaDistance.word_distance import WordDistance

class TestWordDistance(unittest.TestCase):

    def setUp(self):
        """Set up a WordDistance instance for testing."""
        self.wd = WordDistance()

    def test_get_positional(self):
        """Test the get_positional method."""
        with self.subTest("Simple word"):
            result = self.wd.get_positional("la")
            self.assertEqual(result, ('40003', 43))

        with self.subTest("Empty string"):
            result = self.wd.get_positional("")
            self.assertEqual(result, ('', 0))

        with self.subTest("Special characters"):
            result = self.wd.get_positional("@#")
            self.assertEqual(result, ('000000', 0))  # Assuming these are not in mapping

    def test_diff(self):
        """Test the diff method."""
        result = self.wd.diff("laa", "lab")
        self.assertCountEqual(result, ['a', 'b'])

        result = self.wd.diff("abcd", "abef")
        self.assertCountEqual(result, ['c', 'd', 'e', 'f'])

        result = self.wd.diff("", "abcd")
        self.assertCountEqual(result, list("abcd"))

    def test_is_h7q9_swap(self):
        """Test the is_h7q9_swap method."""
        cases = [
            ("7amid", "hamid", True),
            ("9alem", "qalem", True),
            ("salam", "Salam", True),
            ("salam", "salam", True),
            ("salam", "selam", False)
        ]
        for new_word, word, expected in cases:
            with self.subTest(new_word=new_word, word=word):
                result = self.wd.is_h7q9_swap(new_word, word)
                self.assertEqual(result, expected)

    def test_distance_between(self):
        """Test the distance_between method."""
        cases = [
            ("kelb", "kalb", 2.2),
            ("hamid", "7amid", 2.2),
            ("la", "lama", 3.0),
        ]
        for new_word, word, expected in cases:
            with self.subTest(new_word=new_word, word=word):
                result = self.wd.distance_between(new_word, word)
                self.assertAlmostEqual(result, expected)

    def test_get_closests(self):
        """Test the get_closests method."""
        result, min_distance = self.wd.get_closests("kulb")
        self.assertListEqual(result, ['klb', 'kelb', 'kalb'])
        self.assertAlmostEqual(min_distance, 2.1)

    def test_distance_to_confidence(self):
        """Test the distance_to_confidence method."""
        result = self.wd.distance_to_confidence(2.1)
        self.assertAlmostEqual(result, 0.3499377491111553)

        result = self.wd.distance_to_confidence(0)  # Perfect match
        self.assertAlmostEqual(result, 1.0)

    def test_lookup_translation_word(self):
        """Test the lookup_translation_word method."""
        with self.subTest("Known word"):
            result = self.wd.lookup_translation_word("klb")
            self.assertDictEqual(result, {'potential translations': ['dog'], 'confidence': '100%'})

        with self.subTest("Unknown word"):
            result = self.wd.lookup_translation_word("unknownword")
            self.assertEqual(result, {})

        with self.subTest("Name"):
            result = self.wd.lookup_translation_word("aissam")
            self.assertDictEqual(result, {'potential translations': ['Aissam'], 'confidence': '100%'})

    def test_remove_punctuation(self):
        """Test the remove_punctuation method."""
        cases = [
            ("Salam, afin had lghbour!", "Salam afin had lghbour"),
            ("Hello! What's up?", "Hello Whats up"),
            ("", ""),  # Empty string
        ]
        for text, expected in cases:
            with self.subTest(text=text):
                result = self.wd.remove_punctuation(text)
                self.assertEqual(result, expected)

    def test_check_name(self):
        """Test the check_name method."""
        result = self.wd.check_name("aissam")
        self.assertTrue(result[0])
        self.assertDictEqual(result[1], {'potential translations': ['Aissam'], 'confidence': '100%'})

        result = self.wd.check_name("tomobil")
        self.assertFalse(result[0])
        self.assertEqual(result[1], {})

        result = self.wd.check_name("")
        self.assertFalse(result[0])
        self.assertEqual(result[1], {})

    def test_get_all_exact_translations(self):
        """Test the get_all_exact_translations method."""
        result = self.wd.get_all_exact_translations("klb")
        self.assertListEqual(result, ['dog'])

        result = self.wd.get_all_exact_translations("unknown")
        self.assertListEqual(result, [])

if __name__ == '__main__':
    unittest.main()
