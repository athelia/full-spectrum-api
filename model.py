import uuid
from datetime import date, datetime

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped

db = SQLAlchemy()
app = Flask(__name__)


class EggStockRecord(db.Model):
    """Model class for stock records."""

    __tablename__ = "egg_stock_record"

    id: Mapped[uuid.UUID] = db.Column(db.Uuid, primary_key=True)
    created_at: Mapped[datetime] = db.Column(db.DateTime)
    edited_at: Mapped[datetime] = db.Column(db.DateTime)
    record_date: Mapped[date] = db.Column(db.Date)
    quantity: Mapped[int] = db.Column(db.Integer)

    def __repr__(self) -> str:
        # !r returns the repr of the expression
        return f"<EggStockRecord(id={self.id!r}, record_date={self.record_date}, quantity={self.quantity})>"


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
    db_user = input("db user?\n> ")
    db_password = input("db password?\n> ")
    db_host = "localhost"
    db_name = "fullspectrum-dev"
    app.config[
        "SQLALCHEMY_DATABASE_URI"
    ] = f"postgresql://{db_user}:{db_password}@{db_host}/{db_name}"
    db.init_app(app)

    with app.app_context():
        db.drop_all()
        db.create_all()
