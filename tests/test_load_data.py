import unittest

from data.load_data import get_path_for_text_type, parse_text


class LoadDataTests(unittest.TestCase):
    # def test_import_csv_to_db(self, file):
    #     pass
    #
    # def test_import_csv_date_range(self, file, start_date, end_date):
    #     pass

    def test_get_path_for_text_type(self):
        self.assertRaises(KeyError, get_path_for_text_type, "foo")
        about = get_path_for_text_type("about")
        self.assertEqual("../data/about.txt", about)

    def test_parse_text(self):
        self.assertEqual("test output", parse_text("test"))
        # TODO: mock TEXT_SOURCES to add a key/value for an invalid path
        # self.assertRaises(FileNotFoundError, parse_text, "missing")