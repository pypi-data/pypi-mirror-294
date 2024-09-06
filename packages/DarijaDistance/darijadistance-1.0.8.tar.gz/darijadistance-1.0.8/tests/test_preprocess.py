import unittest
from unittest.mock import patch, mock_open
from DarijaDistance.mappings import Mappings
from DarijaDistance.preprocess import DarijaEncoder, DarijaDataManager

class TestDarijaEncoder(unittest.TestCase):

    def setUp(self):
        self.mappings = Mappings()
        self.encoder = DarijaEncoder(self.mappings)

    def test_get_positional(self):
        word = "la"
        positional, sum_image = self.encoder.get_positional(word)
        self.assertEqual(positional, '40003')
        self.assertEqual(sum_image, 43)

    @patch("builtins.open", new_callable=mock_open, read_data="darija,english\nla,no\nklb,dog\n")
    @patch("csv.reader")
    def test_load_csv(self, mock_csv_reader, mock_open_file):
        mock_csv_reader.return_value = [["darija", "english"], ["la", "no"], ["klb", "dog"]]
        self.encoder.load_csv("dummy_path.csv")
        
        # Test if the hash_table_word and hash_table_sum were populated correctly
        self.assertIn("la", self.encoder.hash_table_word)
        self.assertIn(43, self.encoder.hash_table_sum)

    @patch("builtins.open", new_callable=mock_open)
    @patch("pickle.dump")
    def test_save_to_pickle(self, mock_pickle, mock_open_file):
        self.encoder.save_to_pickle("word_path.pickle", "sum_path.pickle", "keys_path.pickle")
        
        mock_open_file.assert_called()
        mock_pickle.assert_called()

class TestDarijaDataManager(unittest.TestCase):

    def setUp(self):
        self.manager = DarijaDataManager()

    @patch("builtins.open", new_callable=mock_open, read_data="names\nAli\nSara\n")
    @patch("os.path.exists", return_value=True)
    def test_add_name(self, mock_exists, mock_open_file):
        self.manager.add_name("Zineb")
        
        # Capture the actual written content
        written_content = [call.args[0].strip().lower() for call in mock_open_file().write.call_args_list]
        
        # Check if 'zineb' is in the written content
        self.assertIn('zineb', written_content)

    @patch("builtins.open", new_callable=mock_open, read_data="darija,english\nla,no\nklb,dog\n")
    @patch("os.path.exists", return_value=True)
    @patch("DarijaDistance.preprocess.DarijaEncoder.load_csv")
    @patch("DarijaDistance.preprocess.DarijaEncoder.save_to_pickle")
    def test_add_translations(self, mock_save_to_pickle, mock_load_csv, mock_exists, mock_open_file):
        translations = [("ma", "water")]
        self.manager.add_translations(translations)
        
        # Capture the actual written content and normalize newlines
        written_content = [call.args[0].replace('\r\n', '\n') for call in mock_open_file().write.call_args_list]
        
        # Assert that the expected string is in the actual calls
        self.assertIn("ma,water\n", written_content)

if __name__ == "__main__":
    unittest.main()
