import unittest

from api.model import Recipe, RecipeIngredient
from data.load_data import create_custard_recipe, get_path_for_text_type, parse_text


class LoadDataTests(unittest.TestCase):
    def test_get_path_for_text_type(self):
        self.assertRaises(KeyError, get_path_for_text_type, "foo")
        about = get_path_for_text_type("about")
        self.assertEqual("../data/about.txt", about)

    def test_parse_text(self):
        self.assertEqual("test output", parse_text("test"))
        self.assertRaises(KeyError, parse_text, "missing")
        # TODO: mock TEXT_SOURCES to add a key/value for an invalid path
        self.assertEqual(
            parse_text("about"), "Full Spectrum Eggs is based in Clarkston, Georgia."
        )

    def test_create_custard_recipe(self):
        c = create_custard_recipe()
        self.assertEqual(type(c), Recipe)
        self.assertEqual(len(c.ingredients), 4)
        self.assertEqual(type(c.ingredients[0]), RecipeIngredient)
        self.assertEqual(c.name, "Custard Pudding (Steamed)")
