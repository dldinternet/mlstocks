import argparse
import datetime
import mock
import sys
from mlstocks.common import input
from mlstocks.common.args import instrument, date_time

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
