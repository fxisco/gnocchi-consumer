import datetime
import time


def getTimeInSeconds(granularity):
    x = time.strptime(granularity,'%H:%M:%S')

    return datetime.timedelta(hours=x.tm_hour,minutes=x.tm_min,seconds=x.tm_sec).total_seconds()

def getLastDateOfMonth():
    any_date = datetime.date.today()

    # Guaranteed to get the next month. Force any_date to 28th and then add 4 days.
    next_month = any_date.replace(day=28) + datetime.timedelta(days=4)

    # Subtract all days that are over since the start of the month.
    last_day_of_month = next_month - datetime.timedelta(days=next_month.day)

    return last_day_of_month
