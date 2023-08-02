import uuid
from datetime import date, datetime
from typing import Dict, List

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped

db = SQLAlchemy()
app = Flask(__name__)


class EggStockRecord(db.Model):
    """Model class for stock records."""

    __tablename__ = "egg_stock_records"

    id: Mapped[uuid.UUID] = db.Column(db.Uuid, primary_key=True)
    created_at: Mapped[datetime] = db.Column(db.DateTime)
    edited_at: Mapped[datetime] = db.Column(db.DateTime)
    record_date: Mapped[date] = db.Column(db.Date)
    quantity: Mapped[int] = db.Column(db.Integer)

    def __repr__(self) -> str:
        # !r returns the repr of the expression
        return f"<EggStockRecord(id={self.id!r}, record_date={self.record_date}, quantity={self.quantity})>"


class Ingredient(db.Model):
    """Model class for ingredients of recipes (to enable scalability)."""

    __tablename__ = "ingredients"

    id: Mapped[uuid.UUID] = db.Column(db.Uuid, primary_key=True)
    created_at: Mapped[datetime] = db.Column(db.DateTime)
    edited_at: Mapped[datetime] = db.Column(db.DateTime)
    name: Mapped[str] = db.Column(db.String)
    ingredient_recipes = db.Relationship()  # legal?

    def to_json(self) -> Dict:
        return {
            "id": self.id,
            "created_at": self.created_at,
            "edited_at": self.edited_at,
            "name": self.name,
        }

    def __init__(self, name):
        super().__init__(
            id=uuid.uuid4(),
            created_at=datetime.utcnow(),
            edited_at=datetime.utcnow(),
            name=name,
        )

    def __repr__(self) -> str:
        return f"<Ingredient(id={self.id!r}, name={self.name})>"


class Recipe(db.Model):
    __tablename__ = "recipes"

    id: Mapped[uuid.UUID] = db.Column(db.Uuid, primary_key=True)
    created_at: Mapped[datetime] = db.Column(db.DateTime)
    edited_at: Mapped[datetime] = db.Column(db.DateTime)
    name: Mapped[str] = db.Column(db.String)
    ingredients: Mapped[List[Ingredient]] = db.Relationship(
        "Ingredient", backref="recipes", secondary="ingredients_recipes"
    )
    instructions: Mapped[str] = db.Column(db.String)
    servings: Mapped[int] = db.Column(db.Integer)
    source: Mapped[str] = db.Column(db.String)

    def to_json(self) -> Dict:
        return {
            "id": self.id,
            "created_at": self.created_at,
            "edited_at": self.edited_at,
            "name": self.name,
            "ingredients": self.ingredients,
            "instructions": self.instructions,
            "servings": self.servings,
            "source": self.source,
        }

    def __init__(self, name, instructions, servings, source):
        super().__init__(
            id=uuid.uuid4(),
            created_at=datetime.utcnow(),
            edited_at=datetime.utcnow(),
            name=name,
            instructions=instructions,
            servings=servings,
            source=source,
        )

    def __repr__(self) -> str:
        return f"<Recipe(id={self.id!r}, name={self.name})>"


class IngredientRecipe(db.Model):
    """Association table for ingredients and recipes. Also specifies quantity of ingredient."""

    __tablename__ = "ingredients_recipes"

    id: Mapped[uuid.UUID] = db.Column(db.Uuid, primary_key=True)
    ingredient_id: Mapped[uuid.UUID] = db.Column(
        db.Uuid, db.ForeignKey("ingredients.id"), nullable=False
    )
    ingredient_qty: Mapped[int] = db.Column(db.Integer)
    ingredient_units: Mapped[str] = db.Column(
        db.String
    )  # TODO maybe: make a units table
    recipe_id: Mapped[uuid.UUID] = db.Column(
        db.Uuid, db.ForeignKey("recipes.id"), nullable=False
    )

    def to_json(self) -> Dict:
        return {
            "id": self.id,
            "ingredient_id": self.ingredient_id,
            "ingredient_qty": self.ingredient_qty,
            "ingredient_units": self.ingredient_units,
            "recipe_id": self.recipe_id,
        }

    def __init__(self, ingredient_id, ingredient_qty, ingredient_units, recipe_id):
        super().__init__(
            id=uuid.uuid4(),
            ingredient_id=ingredient_id,
            ingredient_qty=ingredient_qty,
            ingredient_units=ingredient_units,
            recipe_id=recipe_id,
        )

    def __repr__(self) -> str:
        return (
            f"<IngredientRecipe(id={self.id!r}, ingredient_id={self.ingredient_id},"
            f"ingredient_qty={self.ingredient_qty}, ingredient_units={self.ingredient_units},recipe_id={self.recipe_id})>"
        )


def connect_to_db(application):
    application.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///fullspectrum-dev"
    application.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = application
    db.init_app(application)
    app.app_context().push()


if __name__ == "__main__":
    # import os
    #
    # try:
    #     db_user, db_password = os.environ["DB_USER"], os.environ["DB_PASSWORD"]
    #     db_host, db_name = os.environ["DB_HOST"], os.environ["DB_NAME"]
    # except KeyError:
    #     print(
    #         "DB environmental variables not set. Specify DB_USER, DB_PASSWORD, DB_HOST, and DB_NAME in .env"
    #     )
    #     raise
    # db_user = input("db user?\n> ")
    # db_password = input("db password?\n> ")
    # db_host = "localhost"
    # db_name = "fullspectrum-dev"
    # app.config[
    #     "SQLALCHEMY_DATABASE_URI"
    # ] = f"postgresql://{db_user}:{db_password}@{db_host}/{db_name}"
    # db.init_app(app)
    connect_to_db(app)
    db.create_all()
