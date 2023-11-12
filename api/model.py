import uuid
from datetime import date, datetime
from typing import Dict, List, Optional

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped, relationship

db = SQLAlchemy()
app = Flask(__name__)


# WIP: v1 for current sprint
class Product(db.Model):
    """Model class for products."""

    __tablename__ = "products"

    id: Mapped[uuid.UUID] = db.Column(db.Uuid, primary_key=True)
    created_at: Mapped[datetime] = db.Column(db.DateTime)
    edited_at: Mapped[datetime] = db.Column(db.DateTime)
    name: Mapped[str] = db.Column(db.String)

    production_records: Mapped[List["ProductionRecord"]] = relationship(
        back_populates="product"
    )
    inventory_records: Mapped[List["InventoryRecord"]] = relationship(
        back_populates="product"
    )

    def to_json(self) -> Dict:
        return {
            "id": self.id,
            "created_at": self.created_at,
            "edited_at": self.edited_at,
            "name": self.name,
            "production_records": [
                record.to_json() for record in self.production_records
            ],
            "inventory_records": [
                record.to_json() for record in self.inventory_records
            ],
        }

    def __init__(self, name):
        super().__init__(
            id=uuid.uuid4(),
            created_at=datetime.utcnow(),
            edited_at=datetime.utcnow(),
            name=name,
        )

    def __repr__(self) -> str:
        # !r returns the repr of the expression
        return f"<ProductionRecord(id={self.id!r}, name={self.name})>"


class InventoryRecord(db.Model):
    """Model class for inventory records: available products at a point in time."""

    __tablename__ = "inventory_records"

    id: Mapped[uuid.UUID] = db.Column(db.Uuid, primary_key=True)
    created_at: Mapped[datetime] = db.Column(db.DateTime)
    edited_at: Mapped[datetime] = db.Column(db.DateTime)
    record_date: Mapped[datetime] = db.Column(db.DateTime)
    product_id: Mapped[uuid.UUID] = db.Column(
        db.Uuid, db.ForeignKey("products.id"), nullable=False
    )
    quantity: Mapped[int] = db.Column(db.Integer)
    expiry: Mapped[Optional[datetime]] = db.Column(db.DateTime)

    product: Mapped[Product] = relationship(back_populates="inventory_records")

    def to_json(self) -> Dict:
        return {
            "id": self.id,
            "created_at": self.created_at,
            "edited_at": self.edited_at,
            "record_date": self.record_date,
            "product": self.product.to_json(),
            "quantity": self.quantity,
            "expiry": self.expiry,
        }

    def __init__(self, record_date, product_id, quantity, expiry=None):
        super().__init__(
            id=uuid.uuid4(),
            created_at=datetime.utcnow(),
            edited_at=datetime.utcnow(),
            record_date=record_date,
            product_id=product_id,
            quantity=quantity,
            expiry=expiry,
        )

    def __repr__(self) -> str:
        return (
            f"<ProductionRecord(id={self.id!r}, record_date={self.record_date},"
            f" product_id={self.product_id}, quantity={self.quantity},"
            f" expiry={self.expiry})>"
        )


class ProductionRecord(db.Model):
    """Model class for production records: amount of product produced each interval."""

    __tablename__ = "production_records"

    id: Mapped[uuid.UUID] = db.Column(db.Uuid, primary_key=True)
    created_at: Mapped[datetime] = db.Column(db.DateTime)
    edited_at: Mapped[datetime] = db.Column(db.DateTime)
    product_id: Mapped[uuid.UUID] = db.Column(
        db.Uuid, db.ForeignKey("products.id"), nullable=False
    )
    record_date: Mapped[date] = db.Column(db.Date, unique=True)
    quantity: Mapped[int] = db.Column(db.Integer)

    product: Mapped[Product] = relationship(back_populates="production_records")

    def to_json(self) -> Dict:
        return {
            "id": self.id,
            "created_at": self.created_at,
            "edited_at": self.edited_at,
            "record_date": self.record_date,
            "quantity": self.quantity,
            "product": self.product.to_json(),
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
        return (
            f"<ProductionRecord(id={self.id!r}, record_date={self.record_date},"
            f" quantity={self.quantity}, product_id={self.product_id})>"
        )


# WIP Order table - v1 for stock estimation algorithm
class Order(db.Model):
    """Model class for customer orders."""

    __tablename__ = "orders"

    id: Mapped[uuid.UUID] = db.Column(db.Uuid, primary_key=True)
    created_at: Mapped[datetime] = db.Column(db.DateTime)
    edited_at: Mapped[datetime] = db.Column(db.DateTime)
    order_date: Mapped[date] = db.Column(db.Date)
    order_time: Mapped[datetime] = db.Column(db.DateTime)
    customer_id: Mapped[uuid.UUID] = db.Column(
        db.Uuid, db.ForeignKey("customers.id"), nullable=False
    )
    quantity: Mapped[int] = db.Column(db.Integer)
    product_id: Mapped[uuid.UUID] = db.Column(
        db.Uuid, db.ForeignKey("products.id"), nullable=False
    )
    delivery_pickup: Mapped[str] = db.Column(db.String)
    delivery_address: Mapped[str] = db.Column(db.String)

    customer: Mapped["Customer"] = relationship(back_populates="orders")

    def to_json(self) -> Dict:
        return {
            "id": self.id,
            "created_at": self.created_at,
            "edited_at": self.edited_at,
            "order_date": self.order_date,
            "order_time": self.order_time,
            "customer": self.customer.to_json(),
            "quantity": self.quantity,
        }

    def __init__(
        self,
        order_date,
        order_time,
        customer_id,
        quantity,
        delivery_pickup,
        delivery_address,
    ):
        super().__init__(
            id=uuid.uuid4(),
            created_at=datetime.utcnow(),
            edited_at=datetime.utcnow(),
            order_date=order_date,
            order_time=order_time,
            customer_id=customer_id,
            quantity=quantity,
            delivery_pickup=delivery_pickup,
            delivery_address=delivery_address,
        )

    def __repr__(self) -> str:
        return (
            f"<Order(id={self.id!r}, order_date={self.record_date},"
            f" customer_id={self.customer_id}, quantity={self.quantity})>"
        )


# WIP
class Customer(db.Model):
    """Model class for customers."""

    __tablename__ = "customers"

    id: Mapped[uuid.UUID] = db.Column(db.Uuid, primary_key=True)
    created_at: Mapped[datetime] = db.Column(db.DateTime)
    edited_at: Mapped[datetime] = db.Column(db.DateTime)

    orders: Mapped[List[Order]] = relationship(back_populates="customer")

    def to_json(self) -> Dict:
        return {}

    def __init__(self):
        super().__init__(
            id=uuid.uuid4(),
            created_at=datetime.utcnow(),
            edited_at=datetime.utcnow(),
        )

    def __repr__(self) -> str:
        return f"<Customer(id={self.id!r})>"


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
    """Model class for recipes."""

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
    recipe: Mapped[Recipe] = relationship(back_populates="ingredients")

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
            f"<RecipeIngredient(id={self.id!r},"
            f" abstract_ingredient_id={self.abstract_ingredient_id},quantity={self.quantity},"
            f" units={self.units},recipe_id={self.recipe_id})>"
        )


def connect_to_db(application, uri):
    application.config["SQLALCHEMY_DATABASE_URI"] = uri
    application.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = application
    db.init_app(application)
    app.app_context().push()


# exclude from coverage
if __name__ == "__main__":  # pragma: no cover
    # FIXME to use a configured URI based on dev/prod
    connect_to_db(app, "postgresql:///fullspectrum-dev")
    db.drop_all()
    db.create_all()
