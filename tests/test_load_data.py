import datetime
import io
import unittest

from api.model import Recipe, RecipeIngredient, ProductionRecord
from data.load_data import (
    create_custard_recipe,
    read_daily_egg_csvs,
    convert_daily_eggs_to_weekly_dozens,
)


class LoadDataTests(unittest.TestCase):
    def test_create_custard_recipe(self):
        c = create_custard_recipe()
        self.assertEqual(type(c), Recipe)
        self.assertEqual(len(c.ingredients), 4)
        self.assertEqual(type(c.ingredients[0]), RecipeIngredient)
        self.assertEqual(c.name, "Custard Pudding (Steamed)")

    def test_read_daily_egg_csvs(self):
        s = """05/15/2021,1,7,6,14,\n05/16/2021,1,5,6,12,\n05/17/2021,1,6,5,12,\n05/18/2021,1,6,6,13,\n05/19/2021,1,2,5,8,\n05/20/2021,1,5,6,12,\n05/21/2021,1,5,7,13,\n05/22/2021,,6,4,10,\n05/23/2021,1,6,5,12,\n05/24/2021,1,5,5,11,\n05/25/2021,1,5,6,12,"""
        mock_text = io.StringIO(s)
        daily_records = read_daily_egg_csvs(mock_text)
        date_1 = datetime.date(2021, 5, 15)
        self.assertTupleEqual(daily_records[0], (date_1, 14))
        self.assertEqual(len(daily_records), 11)
        date_2 = datetime.date(2021, 5, 16)
        date_3 = datetime.date(2021, 5, 18)
        mock_text_again = io.StringIO(s)
        limited_records = read_daily_egg_csvs(
            mock_text_again, start_date=date_2, end_date=date_3
        )
        self.assertTupleEqual(limited_records[0], (date_2, 12))
        self.assertTupleEqual(limited_records[-1], (date_3, 13))
        self.assertEqual(len(limited_records), 3)

    def test_convert_daily_eggs_to_weekly_dozens(self):
        mock_egg_records = [
            (datetime.date(2021, 5, 15), 14),
            (datetime.date(2021, 5, 16), 12),
            (datetime.date(2021, 5, 17), 12),
            (datetime.date(2021, 5, 18), 13),
            (datetime.date(2021, 5, 19), 8),
            (datetime.date(2021, 5, 20), 12),
            (datetime.date(2021, 5, 21), 13),
            (datetime.date(2021, 5, 22), 10),
            (datetime.date(2021, 5, 23), 12),
            (datetime.date(2021, 5, 24), 11),
            (datetime.date(2021, 5, 25), 12),
        ]
        db_records = convert_daily_eggs_to_weekly_dozens(mock_egg_records)
        self.assertEqual(len(db_records), 2)
        self.assertEqual(type(db_records[0]), ProductionRecord)
        record_0517 = db_records[0]
        self.assertEqual(record_0517.record_date, datetime.date(2021, 5, 17))
        self.assertEqual(record_0517.quantity, 3)
        record_0524 = db_records[-1]
        self.assertEqual(record_0524.record_date, datetime.date(2021, 5, 24))
        self.assertEqual(record_0524.quantity, 6)
