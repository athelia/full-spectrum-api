import unittest

from api.model import Recipe, RecipeIngredient
from data.load_data import create_custard_recipe


class LoadDataTests(unittest.TestCase):
    def test_create_custard_recipe(self):
        c = create_custard_recipe()
        self.assertEqual(type(c), Recipe)
        self.assertEqual(len(c.ingredients), 4)
        self.assertEqual(type(c.ingredients[0]), RecipeIngredient)
        self.assertEqual(c.name, "Custard Pudding (Steamed)")
