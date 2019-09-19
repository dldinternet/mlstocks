import argparse
import datetime

from mlstocks.common.args import date_time, instrument


class TestCommonArgs():
    def test_instrument(self):
        assert instrument('some/path') == 'some_path'

    def test_date_time(self):
        assert date_time("2019-09-18 00:45:35") == datetime.datetime(2019, 9, 18, 0, 45, 35)

    def test_date_time_valueerror(self):
        try:
            date_time("%Y-%m-%d %H:%M:%S")
        except argparse.ArgumentTypeError as ate:
            assert ate.args[0] == "Not a valid date: '%Y-%m-%d %H:%M:%S'."
        return False
