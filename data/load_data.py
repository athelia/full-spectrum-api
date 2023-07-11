import logging
import uuid
from datetime import datetime
from pprint import pprint
from typing import List

from model import EggStockRecord, app, db

log = logging.Logger("LoadData")

TEXT_SOURCES = {"about": "../data/about.txt", "test": "../tests/test.txt"}


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
                id=uuid.uuid4(),
                created_at=datetime.now(),
                edited_at=datetime.now(),
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
    db_user = input("db user?\n> ")
    db_password = input("db password?\n> ")
    db_host = "localhost"
    db_name = "fullspectrum-dev"
    app.config[
        "SQLALCHEMY_DATABASE_URI"
    ] = f"postgresql://{db_user}:{db_password}@{db_host}/{db_name}"
    db.init_app(app)
    with app.app_context():
        records = import_csv_to_db("20230119.csv", end_date=datetime(2023, 1, 1))
        pprint(f"head: {records[:5]}, tail: {records[-5:]}")
