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


# is the `birth_date` `greater` than `age` now?
def is_age(age: int, greater: bool, birth_date: datetime = None):
    if isinstance(birth_date, datetime):
        if greater:
            return years_ago(age, datetime.now()) >= birth_date
        else:
            return years_ago(age, datetime.now()) <= birth_date
        # Would be a one line function if it weren't for you meddling kids and your error checking
    else:
        raise TypeError("I need a date. Desperately.")  # (JDG) Ask a silly question, get a silly answer.



def date_to_datetime(date):
    return datetime.combine(date, datetime.min.time())


# date_to_datetime(datetime.strptime('Jul 18 1001', '%b %d %Y'))



print(is_age(18, False, date_to_datetime(datetime.strptime('Jul 18 2011', '%b %d %Y'))))
# print(is_age(123, True, date_to_datetime(datetime.strptime('Jul 18 2020', '%b %d %Y'))))