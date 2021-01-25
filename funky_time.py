#  handy functions for doing the heavy lifting in the nightmare that is the global datetime system

from datetime import datetime
from time import gmtime


# what date is x years from a given date?
def years_ago(years: int, from_date: datetime = None):
    if from_date is None:
        from_date = datetime.now()
    try:
        return from_date.replace(year=from_date.year - years)
    except ValueError:
        # Must be 2/29!
        assert from_date.month == 2 and from_date.day == 29  # can be removed
        return from_date.replace(month=2, day=28, year=from_date.year - years)


def is_younger_than(age: int, birth_date: datetime = None):
    return years_ago(age, datetime.now()) <= birth_date


def is_older_than(age: int, birth_date: datetime = None):
    return years_ago(age, datetime.now()) >= birth_date


def date_to_datetime(date):
    return datetime.combine(date, datetime.min.time())


def epoch_to_datetime(time):
    return datetime.timestamp(time)
