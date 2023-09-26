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


def create_custard_recipe() -> Recipe:
    """Create steamed custard recipe with four AbstractIngredients + RecipeIngredients.
    :return: custard Recipe SQLAlchemy object with connected RecipeIngredients and AbstractIngredients
    """
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
    _ = [
        RecipeIngredient(
            abstract_ingredient=AbstractIngredient(name=name),
            quantity=qty,
            units=units,
            recipe=custard,
        )
        for name, qty, units in [
            ["egg", 4, "ea"],
            ["milk", 500, "mL"],
            ["sugar", 125, "g"],
            ["water", 125, "mL"],
        ]
    ]
    return custard


def handle_import(type: str, file: str) -> Union[List[EggStockRecord], List[Recipe], List[RecipeIngredient]]:
    lines = import_csv(file)
    fields = format_fields(type, lines)
    model_objects = make_model_objects(type, fields)
    return model_objects


def import_csv(file: str) -> str:
    with open(file) as f:
        # This assumes a header line
        relevant_lines = [line.split(",") for line in f[1:]]
        return relevant_lines


def format_fields(type: str, lines: str) -> List:
    if type == "egg":
        fields = [
            [datetime.strptime(line[0], "%m/%d/%Y"), sum(int(line[4]), int(line[5]))]
            for line in lines
        ]
    elif type == "recipe":
        fields = [
            [int(line[0]), line[1], line[2], int(line[3]), line[4], line[5]] for line in lines
        ]
    elif type == "recipe_ingredient":
        fields = [
            [line[0], int(line[1]) if line[1] else int(line[3]), line[2] if line[2] else line[4], int(line[5])] for line in lines
        ]
    else:
        raise NameError("No such type")
    return fields


def make_model_objects(type: str, fields: List) -> Union[List[EggStockRecord], List[Recipe], List[RecipeIngredient]]:
    if type == "egg":
        egg_records = [EggStockRecord(
            record_date=line[0],
            quantity=line[1],
        )
            for line in fields
        ]
        return egg_records
    elif type == "recipe":
        recipes = [Recipe(name=name, instructions=instructions, servings=servings, source=source, photo=photo) for _, name, instructions, servings, source, photo in fields]
        return recipes
    elif type == "recipe_ingredient":
        recipe_ingredients = [RecipeIngredient(
                abstract_ingredient=AbstractIngredient(name=name),
                quantity=qty,
                units=units,
                recipe=_,  # FIXME
            )
            for name, qty, units, recipe in fields
            ]
        return recipe_ingredients


# TODO: generalize import_csv and route to helper fns depending on data type
def import_egg_record_csv_to_db(
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


if __name__ == "__main__":
    connect_to_db(app)
    with app.app_context():
        records = import_egg_record_csv_to_db("2022.csv")
        pprint(f"head: {records[:5]}, tail: {records[-5:]}")
        c = create_custard_recipe()
        db.session.add(c)
        db.session.commit()
