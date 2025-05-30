from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

DATE_FORMAT = "%Y-%m-%d"
QUARTER_FORMAT = "%Y-%Q"  # invalid strf format e.g. 2024-3


def get_quarter_end_date(quarter_string):
    year, quarter = map(int, quarter_string.split("-"))
    end_month = quarter * 3
    end_date = datetime(year, end_month, 1) + relativedelta(months=1, days=-1)
    return end_date


def get_rebalance_date(quarter_string):
    """
    If quarter end date is Sep 30 2024, i.e. 2024-3
    The (flawed) assumption is that the Edinet documents will be released by the first business day of Nov.
    The companies have a month to produce doc.


    """
    quarter_end_date = get_quarter_end_date(quarter_string)
    next_month_start = quarter_end_date + relativedelta(months=1, days=1)

    # Work forward from the first day of the next month to find the first business day
    current_date = next_month_start

    while True:
        # Check if the current date is a weekday (Monday=0, Sunday=6)
        if current_date.weekday() < 5:  # Monday to Friday
            return current_date.strftime(DATE_FORMAT)
        current_date += timedelta(days=1)
