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


# using years_ago, is this person 18 years old, or older, right now?
def is_18(birth_date: datetime = None):
    if isinstance(birth_date, datetime):
        return years_ago(18, datetime.now()) > birth_date
        # Would be a one line function if it weren't for you meddling kids and your error checking
        # (JDG) Used > just for clarity. Could arguably be >=
    else:
        raise TypeError("I need a date. Desperately.")  # (JDG) Ask a silly question, get a silly answer.


def date_to_datetime(date):
    return datetime.combine(date, datetime.min.time())


# print(date_to_datetime(datetime.strptime('Jul 18 2001', '%b %d %Y')))