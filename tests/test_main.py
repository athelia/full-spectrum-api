import datetime
import json

import pytest

from main import app
from model import Recipe


@pytest.fixture()
def client():
    app.config.update(
        {
            "TESTING": True,
        }
    )
    return app.test_client()


def test_index(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"welcome to full spectrum eggs" in response.data


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


class MockQuery:
    @staticmethod
    def get(*args, **kwargs):
        return MockFruitPieRecipe()

    @staticmethod
    def all(*args, **kwargs):
        return [MockFruitPieRecipe(), MockPilafRecipe()]


def test_get_single_recipe(client, monkeypatch):
    with app.app_context():
        monkeypatch.setattr(Recipe, "query", MockQuery)
        response = client.get("/recipe/fruit_pie_id")
        assert response.status_code == 200
        data_dict = json.loads(response.data)
        assert len(data_dict) == 8
        assert data_dict.get("name") == "fruit pie"
        assert data_dict.get("ingredients")[0].get("name") == "hearty durian"


def test_get_all_recipes(client, monkeypatch):
    with app.app_context():
        monkeypatch.setattr(Recipe, "query", MockQuery)
        response = client.get("/recipes")
        assert response.status_code == 200
        data_dicts = json.loads(response.data)
        assert len(data_dicts) == 2
        assert data_dicts[0].get("name") == "fruit pie"
        assert data_dicts[1].get("ingredients")[0].get("name") == "hylian rice"
