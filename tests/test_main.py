import datetime
import json

import pytest

from api.main import app
from api.model import Recipe, EggStockRecord


@pytest.fixture()
def client():
    app.config.update(
        {
            "TESTING": True,
        }
    )
    return app.test_client()


uris_and_response_strings = [
    ("/api/", b"welcome to full spectrum eggs"),
    ("/api/about", b"Full Spectrum Eggs is based in Clarkston, Georgia."),
]


@pytest.mark.parametrize("uri,response_string", uris_and_response_strings)
def test_static_routes(client, uri, response_string):
    response = client.get(uri)
    assert response.status_code == 200
    assert response_string in response.data


class MockFruitPieRecipe:
    @staticmethod
    def to_json():
        date = datetime.date(2023, 1, 1)
        return {
            "id": "fruit_pie_id",
            "created_at": date,
            "edited_at": date,
            "name": "fruit pie",
            "ingredients": [
                {
                    "id": "ingredient_1",
                    "abstract_ingredient_id": "abstract_1",
                    "recipe_id": "fruit_pie_id",
                    "name": "hearty durian",
                    "quantity": 1,
                    "units": "ea",
                },
                {
                    "id": "ingredient_2",
                    "abstract_ingredient_id": "abstract_2",
                    "recipe_id": "fruit_pie_id",
                    "name": "tabantha wheat",
                    "quantity": 300,
                    "units": "g",
                },
                {
                    "id": "ingredient_3",
                    "abstract_ingredient_id": "abstract_3",
                    "recipe_id": "fruit_pie_id",
                    "name": "cane sugar",
                    "quantity": 200,
                    "units": "g",
                },
                {
                    "id": "ingredient_4",
                    "abstract_ingredient_id": "abstract_4",
                    "recipe_id": "fruit_pie_id",
                    "name": "goat butter",
                    "quantity": 1,
                    "units": "stick",
                },
            ],
            "instructions": "Combine all ingredients in pot",
            "servings": 1,
            "source": "http://botw-recipes.com/",
        }


class MockPilafRecipe:
    @staticmethod
    def to_json():
        date = datetime.date(2023, 1, 1)
        return {
            "id": "gourmet_poultry_pilaf_id",
            "created_at": date,
            "edited_at": date,
            "name": "gourmet poultry pilaf",
            "ingredients": [
                {
                    "id": "ingredient_5",
                    "abstract_ingredient_id": "abstract_5",
                    "recipe_id": "gourmet_poultry_pilaf_id",
                    "name": "hylian rice",
                    "quantity": 350,
                    "units": "g",
                },
                {
                    "id": "ingredient_6",
                    "abstract_ingredient_id": "abstract_6",
                    "recipe_id": "gourmet_poultry_pilaf_id",
                    "name": "bird egg",
                    "quantity": 2,
                    "units": "ea",
                },
                {
                    "id": "ingredient_7",
                    "abstract_ingredient_id": "abstract_4",
                    "recipe_id": "gourmet_poultry_pilaf_id",
                    "name": "goat butter",
                    "quantity": 0.5,
                    "units": "stick",
                },
                {
                    "id": "ingredient_8",
                    "abstract_ingredient_id": "abstract_8",
                    "recipe_id": "gourmet_poultry_pilaf_id",
                    "name": "raw whole bird",
                    "quantity": 1,
                    "units": "ea",
                },
            ],
            "instructions": "Combine all ingredients in pot",
            "servings": 1,
            "source": "http://botw-recipes.com/",
        }


class MockRecipeQuery:
    @staticmethod
    def get(*args, **kwargs):
        return MockFruitPieRecipe()

    @staticmethod
    def all(*args, **kwargs):
        return [MockFruitPieRecipe(), MockPilafRecipe()]


class MockEggStockRecord1:
    @staticmethod
    def to_json():
        date = datetime.date(2023, 1, 1)
        return {
            "id": "record_1_id",
            "created_at": date,
            "edited_at": date,
            "record_date": datetime.date(2021, 1, 1),
            "quantity": 3,
        }


class MockEggStockRecord2:
    @staticmethod
    def to_json():
        date = datetime.date(2023, 1, 1)
        return {
            "id": "record_1_id",
            "created_at": date,
            "edited_at": date,
            "record_date": datetime.date(2021, 1, 8),
            "quantity": 6,
        }


class MockEggStockRecordQuery:
    @staticmethod
    def all(*args, **kwargs):
        return [MockEggStockRecord1(), MockEggStockRecord2()]


def test_get_single_recipe(client, monkeypatch):
    with app.app_context():
        monkeypatch.setattr(Recipe, "query", MockRecipeQuery)
        response = client.get("/api/recipe/fruit_pie_id")
        assert response.status_code == 200
        data_dict = json.loads(response.data)
        assert len(data_dict) == 8
        assert data_dict.get("name") == "fruit pie"
        assert data_dict.get("ingredients")[0].get("name") == "hearty durian"


def test_get_all_recipes(client, monkeypatch):
    with app.app_context():
        monkeypatch.setattr(Recipe, "query", MockRecipeQuery)
        response = client.get("/api/recipes")
        assert response.status_code == 200
        data_dicts = json.loads(response.data)
        assert len(data_dicts) == 2
        assert data_dicts[0].get("name") == "fruit pie"
        assert data_dicts[1].get("ingredients")[0].get("name") == "hylian rice"


def test_get_egg_stock_records(client, monkeypatch):
    with app.app_context():
        monkeypatch.setattr(EggStockRecord, "query", MockEggStockRecordQuery)
        response = client.get("/api/egg-stock-records")
        assert response.status_code == 200
        data_dicts = json.loads(response.data)
        assert len(data_dicts) == 2
        assert data_dicts[0].get("quantity") == 3
        record_date = (
            datetime.datetime.strptime(
                data_dicts[1].get("record_date"), "%a, %d %b %Y %H:%M:%S %Z"
            )
        ).date()
        assert record_date == datetime.date(2021, 1, 8)
