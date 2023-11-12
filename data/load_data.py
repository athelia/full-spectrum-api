import logging
from datetime import datetime, date
from typing import List, TextIO, Tuple

from api.model import (
    AbstractIngredient,
    ProductionRecord,
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


def read_daily_egg_csvs(
    filestream: TextIO,
    start_date: date = date(1, 1, 1),
    end_date: date = date.today(),
) -> List[Tuple[date, int]]:
    """Format CSV data into EggStockRecord and commit to db

    :param filestream: opened csv file
    :param start_date: date of the earliest record to be included
    :param end_date: date of the latest record to be included
    :return: EggStockRecords
    """
    # split at comma delimiter and exclude rows missing dates or quantity data
    relevant_lines = [
        line.split(",")
        for line in filestream
        if line[0][0].isdigit() and line[4].isdigit()
    ]
    # date column must already be in mm/dd/yyyy format
    formatted_fields = [
        (datetime.date(datetime.strptime(line[0], "%m/%d/%Y")), int(line[4]))
        for line in relevant_lines
    ]
    # in order to use a list comp here & above, line[0] must be a date type already
    egg_records = [
        (line[0], line[1])
        for line in formatted_fields
        if start_date <= line[0] <= end_date
    ]
    return egg_records


def convert_daily_eggs_to_weekly_dozens(
    records: List[Tuple[date, int]]
) -> List[ProductionRecord]:
    weekly_records = []
    week_sum = 0
    # sum all eggs harvested per week
    for record in records:
        week_sum += record[1]
        if record[0].weekday() == 0:
            # maintain tuple structure: (date, quantity)
            # round down dozens
            weekly_records.append((record[0], week_sum // 12))
            week_sum = 0

    db_records = [
        ProductionRecord(record_date=wr[0], quantity=wr[1]) for wr in weekly_records
    ]
    return db_records


# exclude from coverage because only file opening is not covered by other unit tests
def file_helper(files: List[str]) -> List[ProductionRecord]:  # pragma: no cover
    db_records = []
    for file in files:
        with open(file) as f:
            egg_records = read_daily_egg_csvs(f)
            db_records += convert_daily_eggs_to_weekly_dozens(egg_records)
    return db_records


# exclude from coverage
if __name__ == "__main__":  # pragma: no cover
    connect_to_db(app)
    with app.app_context():
        user_wants_custard = input("Recreate custard recipe? y/n ")
        user_wants_eggs = input("Recreate egg quantity records? y/n ")
        if user_wants_custard in "yY":
            c = create_custard_recipe()
            db.session.add(c)
        if user_wants_eggs in "yY":
            r = file_helper(["2021.csv", "2022.csv", "2023.csv"])
            db.session.add_all(r)
            print(f"Committing {len(r)} new records")
        db.session.commit()
