import unittest

from model import AbstractIngredient


class TestModels(unittest.TestCase):
    def test_ingredient(self):
        flour = AbstractIngredient(name="flour")
