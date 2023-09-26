import uuid
from datetime import date, datetime
from typing import Dict, List

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped, relationship

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

    def to_json(self) -> Dict:
        return {
            "id": self.id,
            "created_at": self.created_at,
            "edited_at": self.edited_at,
            "record_date": self.record_date,
            "quantity": self.quantity,
        }

    def __init__(self, record_date, quantity):
        super().__init__(
            id=uuid.uuid4(),
            created_at=datetime.utcnow(),
            edited_at=datetime.utcnow(),
            record_date=record_date,
            quantity=quantity,
        )

    def __repr__(self) -> str:
        # !r returns the repr of the expression
        return f"<EggStockRecord(id={self.id!r}, record_date={self.record_date}, quantity={self.quantity})>"


class AbstractIngredient(db.Model):
    """Model class for ingredients of recipes"""

    __tablename__ = "abstract_ingredients"

    id: Mapped[uuid.UUID] = db.Column(db.Uuid, primary_key=True)
    created_at: Mapped[datetime] = db.Column(db.DateTime)
    edited_at: Mapped[datetime] = db.Column(db.DateTime)
    name: Mapped[str] = db.Column(db.String, unique=True)
    recipe_ingredients: Mapped[List["RecipeIngredient"]] = relationship(
        back_populates="abstract_ingredient"
    )

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
        return f"<AbstractIngredient(id={self.id!r}, name={self.name})>"


class Recipe(db.Model):
    __tablename__ = "recipes"

    id: Mapped[uuid.UUID] = db.Column(db.Uuid, primary_key=True)
    created_at: Mapped[datetime] = db.Column(db.DateTime)
    edited_at: Mapped[datetime] = db.Column(db.DateTime)
    name: Mapped[str] = db.Column(db.String)
    instructions: Mapped[str] = db.Column(db.String)
    servings: Mapped[int] = db.Column(db.Integer)
    source: Mapped[str] = db.Column(db.String)
    ingredients: Mapped[List["RecipeIngredient"]] = relationship(
        back_populates="recipe"
    )

    def to_json(self) -> Dict:
        return {
            "id": self.id,
            "created_at": self.created_at,
            "edited_at": self.edited_at,
            "name": self.name,
            "ingredients": [ingredient.to_json() for ingredient in self.ingredients],
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


class RecipeIngredient(db.Model):
    """Association table for ingredients and recipes. Also specifies quantity of ingredient."""

    __tablename__ = "recipe_ingredients"

    id: Mapped[uuid.UUID] = db.Column(db.Uuid, primary_key=True)
    abstract_ingredient_id: Mapped[uuid.UUID] = db.Column(
        db.Uuid, db.ForeignKey("abstract_ingredients.id"), nullable=False
    )
    quantity: Mapped[int] = db.Column(db.Integer)
    units: Mapped[str] = db.Column(db.String)  # TODO maybe: make a units table
    recipe_id: Mapped[uuid.UUID] = db.Column(
        db.Uuid, db.ForeignKey("recipes.id"), nullable=False
    )
    abstract_ingredient: Mapped[AbstractIngredient] = relationship(
        back_populates="recipe_ingredients"
    )
    recipe: Mapped[Recipe] = db.Relationship(back_populates="ingredients")

    def to_json(self) -> Dict:
        return {
            "id": self.id,
            "abstract_ingredient_id": self.abstract_ingredient_id,
            "recipe_id": self.recipe_id,
            "name": self.abstract_ingredient.name,
            "quantity": self.quantity,
            "units": self.units,
        }

    def __init__(
        self, quantity, units, abstract_ingredient=abstract_ingredient, recipe=recipe
    ):
        super().__init__(
            id=uuid.uuid4(),
            quantity=quantity,
            units=units,
            abstract_ingredient=abstract_ingredient,
            recipe=recipe,
        )

    def __repr__(self) -> str:
        return (
            f"<RecipeIngredient(id={self.id!r}, abstract_ingredient_id={self.abstract_ingredient_id},"
            f"quantity={self.quantity}, units={self.units},recipe_id={self.recipe_id})>"
        )


def connect_to_db(application):
    application.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///fullspectrum-dev"
    application.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = application
    db.init_app(application)
    app.app_context().push()


if __name__ == "__main__":
    connect_to_db(app)
    db.drop_all()
    db.create_all()
