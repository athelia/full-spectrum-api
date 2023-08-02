import unittest

from model import Ingredient


class TestModels(unittest.TestCase):
    def test_ingredient(self):
        flour = Ingredient(name="flour")
