import logging
from datetime import datetime
from pprint import pprint
from typing import List

from api.model import (
    AbstractIngredient,
    EggStockRecord,
    Recipe,
    RecipeIngredient,
    app,
    connect_to_db,
    db,
)

log = logging.Logger("LoadData")

TEXT_SOURCES = {"about": "../data/about.txt", "test": "../tests/test.txt"}


def create_custard_recipe() -> None:
    egg = AbstractIngredient(name="egg")
    milk = AbstractIngredient(name="milk")
    sugar = AbstractIngredient(name="sugar")
    water = AbstractIngredient(name="water")
    custard = Recipe(
        name="Custard Pudding (Steamed)",
        instructions="1. Mix rock sugar and water in a saucepan. Boil on low heat, stirring occasionally. Once the "
        "sugar has dissolved, switch off the heat and pour in the fresh milk. Set this aside to cool.\n"
        "2. Beat the eggs gently with a whisk or fork before adding to the mixture. Stir well."
        "Strain egg mixture through a sieve to remove bubbles.\n"
        "3. Once the egg mixture is ready, gently pour it into the moulds or bowls. Use a small spoon to"
        " remove any bubbles on the surface. Wrap the bowls tightly with cling wrap or tin foil.\n"
        "4. Place the bowls into the steamer and steam for 12 minutes. Lift it every few minutes to let "
        "steam escape. Once the egg pudding has set, it is ready to serve.",
        servings=4,
        source="https://www.honestfoodtalks.com/egg-pudding-custard-boba/#ingredients",
    )
    custard_eggs = RecipeIngredient(
        abstract_ingredient=egg,
        quantity=4,
        units="ea",
        recipe=custard,
    )
    custard_milk = RecipeIngredient(
        abstract_ingredient=milk,
        quantity=500,
        units="mL",
        recipe=custard,
    )
    custard_sugar = RecipeIngredient(
        abstract_ingredient=sugar,
        quantity=125,
        units="g",
        recipe=custard,
    )
    custard_water = RecipeIngredient(
        abstract_ingredient=water,
        quantity=125,
        units="mL",
        recipe=custard,
    )
    db.session.add_all([custard_eggs, custard_milk, custard_sugar, custard_water])
    db.session.commit()


def import_csv_to_db(
    file: str,
    start_date: datetime = datetime(1, 1, 1),
    end_date: datetime = datetime.now(),
) -> List[EggStockRecord]:
    """Format CSV data into EggStockRecord and commit to db

    :param file: filename
    :param start_date: date of the earliest record to be included
    :param end_date: date of the latest record to be included
    :return: EggStockRecords committed to db
    """
    with open(file) as f:
        # split at comma delimiter and exclude rows without dates
        relevant_lines = [line.split(",") for line in f if line[0][0].isdigit()]
        # date column must already be in mm/dd/yyyy format
        formatted_fields = [
            [datetime.strptime(line[0], "%m/%d/%Y"), int(line[5])]
            for line in relevant_lines
        ]
        egg_records = [
            EggStockRecord(
                record_date=line[0],
                quantity=line[1],
            )
            for line in formatted_fields
            # if start/end dates specified, write data only between those bounds
            if start_date < line[0] < end_date
        ]
        _ = [db.session.add(record) for record in egg_records]
        db.session.commit()
        print(f"Committed {len(_)} new records")
        return egg_records


def get_path_for_text_type(text_type: str) -> str:
    """From the type of text, return the path.
    :param text_type: kind of text to be retrieved.
    :return: file path corresponding to the type of text
    :raise KeyError for unknown text types
    """
    try:
        source = TEXT_SOURCES[text_type]
    except KeyError as e:
        log.warning(f"Unknown text_type={text_type}")
        raise e
    return source


def parse_text(text_type: str) -> str:
    """Return text of a type from the specified source.
    :param text_type: kind of text to be retrieved.
    :return: content of text
    :raise FileNotFound if the file is invalid
    """
    source = get_path_for_text_type(text_type)
    output = ""
    try:
        with open(file=source) as f:
            # TODO: can use a generator comprehension?
            # output += (line for line in f)
            for line in f:
                output += line
        return output
    except FileNotFoundError as e:
        log.warning(
            f"No file found for text_type{text_type}.",
            f"Available sources: {TEXT_SOURCES}",
        )
        raise e


if __name__ == "__main__":
    connect_to_db(app)
    with app.app_context():
        records = import_csv_to_db("sample.csv", end_date=datetime(2023, 1, 1))
        pprint(f"head: {records[:5]}, tail: {records[-5:]}")
        create_custard_recipe()
