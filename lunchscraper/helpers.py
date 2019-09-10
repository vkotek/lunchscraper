# helpers.py
# Miscellaneous helper functions

from datetime import datetime
import dateutil

def pretty_datetime(datetime_string):
    try:
        foo = dateutil.parser.parse(datetime_string)
        return datetime.strftime( foo, '%Y-%m-%d %H:%M')
    except:
        return "-"
