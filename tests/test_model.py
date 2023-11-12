import unittest

from api.model import AbstractIngredient, app, connect_to_db, db, Product


class TestModels(unittest.TestCase):
    def setUp(self) -> None:
        self.client = app.test_client()
        app.config["TESTING"] = True
        connect_to_db(app, "postgresql:///fullspectrum-test")
        db.create_all()

    def tearDown(self) -> None:
        pass

    def sample_product(self):
        product = Product(name="")
        db.session.add(product)
        db.session.commit()

    def test_product(self):
        self.assertEqual(Product.query.get().name, "")  # FIXME

    def test_ingredient(self):
        flour = AbstractIngredient(name="flour")
        self.assertEqual(flour.name, "flour")
        self.assertIsInstance(flour, AbstractIngredient)
