import argparse
from datetime import datetime


def instrument(i):
    return i.replace("/", "_")


def date_time(date_string, fmt="%Y-%m-%d %H:%M:%S"):
    def parse(s):
        try:
            return datetime.strptime(s, fmt)
        except ValueError:
            msg = "Not a valid date: '{0}'.".format(s)
            raise argparse.ArgumentTypeError(msg)

    return parse(date_string)
