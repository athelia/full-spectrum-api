import uuid
from datetime import datetime
from pprint import pprint
from typing import List

from model import EggStockRecord, app, db


def import_csv_to_db(
    file: str,
    start_date: datetime = datetime(1, 1, 1),
    end_date: datetime = datetime.now(),
) -> List[EggStockRecord]:
    """Format CSV data into EggStockRecord and commit to db

    :argument:
        file (str): filename
        start_date (datetime): date of the earliest record to be included
        end_date (datetime): date of the latest record to be included

    :returns:
        List[EggStockRecord]: EggStockRecords committed to db
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
