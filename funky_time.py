#  handy functions for doing the heavy lifting in the nightmare that is the global datetime system

from datetime import datetime
from django.utils.timezone import make_aware
from time import gmtime
from web.settings import TIME_ZONE

from django.utils.timezone import make_aware


# what date is x years from a given date in the past?
def years_ago(years: int, from_date: datetime = None):
    if from_date is None:
        from_date = datetime.now()
    try:
        return from_date.replace(year=from_date.year - years)
    except ValueError:
        # Must be 2/29!
        assert from_date.month == 2 and from_date.day == 29  # can be removed
        return from_date.replace(month=2, day=28, year=from_date.year - years)


# what date is x years from a given date in the future?
def years_from(years: int, from_date: datetime):
    try:
        new_date = from_date.replace(year=from_date.year + years)
        return make_aware(new_date)
    except ValueError:
        # Must be 2/29!
        new_date = from_date.replace(month=3, day=1, year=from_date.year + years)
        return make_aware(new_date)


def is_younger_than(age: int, birth_date: datetime = None):
    return years_ago(age, datetime.now()) <= birth_date


def is_older_than(age: int, birth_date: datetime = None):
    return years_ago(age, datetime.now()) >= birth_date


def date_to_datetime(date):
    return datetime.combine(date, datetime.min.time())


def epoch_to_datetime(time):
    return make_aware(datetime.fromtimestamp(time))
