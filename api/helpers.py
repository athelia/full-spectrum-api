# Helper functions/calculations for the API
import datetime

from api.model import ProductionRecord, Order


def get_stock_level(date: datetime.date) -> int:
    today = datetime.date.today()
    if date < today:
        return get_historical_stock_level(date)
    else:
        return get_predicted_stock_level(date)


def get_historical_stock_level(date: datetime.date) -> int:
    today = datetime.date.today()
    # get the most recently past weekday 0
    weekday = today.weekday()
    record = ProductionRecord.query.filter(
        ProductionRecord.record_date
        == (today - datetime.timedelta(days=(7 if weekday == 0 else weekday))).date()
    )
    if record:
        # naive calculation is production - orders since production date
        produced = record.quantity
        orders = Order.query.filter(Order.order_date >= record.record_date)
        return produced - sum([order.quantity for order in orders])
    else:
        return get_predicted_stock_level(date)


def get_predicted_stock_level(date: datetime.date) -> int:
    today = datetime.date.today()
    pass
