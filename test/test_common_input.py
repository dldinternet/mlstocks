import argparse
import datetime
import mock
import sys
from mlstocks.common import input
from mlstocks.common.args import instrument, date_time

def rv(*args, **kwargs):
  global invocation_count
  print ('invocation_count={}'.format(invocation_count))
  if invocation_count > 0:
    return 'string'
  else:
    invocation_count += 1
    raise Exception


def yns(*args, **kwargs):
  global invocation_count
  print ('invocation_count={}'.format(invocation_count))
  if invocation_count > 1:
    return 'y'
  elif invocation_count > 0:
    invocation_count += 1
    raise Exception
  else:
    invocation_count += 1
    return 'yn'


def fls(*args, **kwargs):
  global invocation_count
  invocation_count += 1
  print ('invocation_count={}'.format(invocation_count))
  if invocation_count > 1:
    return '1'
  elif invocation_count > 0:
    raise Exception


class TestCommonInput():

  builtin = 'builtins.raw_input'
  try:
    i = raw_input
  except NameError:
    builtin = 'builtins.input'


  # === get_input


  def test_get_input(self):
    with mock.patch(self.builtin, return_value='input'):
      assert input.get_input("prompt") == 'input'


  def test_get_input_systemexit(self):
    with mock.patch('builtins.input', mock.MagicMock(side_effect=SystemExit)):
      try:
        input.get_input("prompt")
      except SystemExit:
        return True


  # === get_string


  def test_get_string(self):

    with mock.patch('mlstocks.common.input.get_input', return_value='get_string'):
      assert input.get_string("prompt") == 'get_string'


  def test_get_string_ki(self):

    with mock.patch('mlstocks.common.input.get_input', mock.MagicMock(side_effect=KeyboardInterrupt)):
      try:
        input.get_string("prompt")
      except SystemExit:
        return True


  def test_get_string_eof(self):

    with mock.patch('mlstocks.common.input.get_input', mock.MagicMock(side_effect=EOFError)):
      try:
        input.get_string("prompt")
      except SystemExit:
        return True


  def test_get_string_se(self):

    with mock.patch('mlstocks.common.input.get_input', mock.MagicMock(side_effect=SystemExit)):
      try:
        input.get_string("prompt")
      except SystemExit:
        return True


  def test_get_string_exc(self):
    global invocation_count
    invocation_count = 0
    with mock.patch('mlstocks.common.input.get_input', mock.MagicMock(side_effect=rv)):
      assert input.get_string("prompt") is 'string'


  # === get_password


  def test_get_password(self):

    with mock.patch('getpass.getpass', return_value='password'):
      assert input.get_password("prompt") == 'password'


  def test_get_password_ki(self):

    for exc in (KeyboardInterrupt, EOFError, SystemExit):
      with mock.patch('getpass.getpass', mock.MagicMock(side_effect=exc)):
        try:
          input.get_password("prompt")
        except SystemExit:
          assert True
    return True


  def test_get_password_exc(self):
    global invocation_count
    invocation_count = 0

    with mock.patch('getpass.getpass', mock.MagicMock(side_effect=rv)):
      assert input.get_password("prompt") is 'string'


  # === get_yn


  def test_get_y_default(self):

    with mock.patch('mlstocks.common.input.get_input', return_value=''):
      assert input.get_yn("prompt", default=True) is True


  def test_get_n_default(self):

    with mock.patch('mlstocks.common.input.get_input', return_value=''):
      assert input.get_yn("prompt", default=False) is False


  def test_get_y(self):

    with mock.patch('mlstocks.common.input.get_input', return_value='y'):
      assert input.get_yn("prompt") is True

    with mock.patch('mlstocks.common.input.get_input', return_value='Y'):
      assert input.get_yn("prompt") is True


  def test_get_n(self):

    with mock.patch('mlstocks.common.input.get_input', return_value='n'):
      assert not input.get_yn("prompt")

    with mock.patch('mlstocks.common.input.get_input', return_value='N'):
      assert not input.get_yn("prompt")


  def test_get_yn_gt_1(self):
    global invocation_count
    invocation_count = 0

    with mock.patch('mlstocks.common.input.get_input', side_effect=yns):
      assert input.get_yn("prompt") is True


  def test_get_yn_exc(self):

    for exc in (KeyboardInterrupt, EOFError, SystemExit):
      with mock.patch('mlstocks.common.input.get_input', mock.MagicMock(side_effect=exc)):
        try:
          input.get_yn("prompt")
        except SystemExit:
          assert True
    return True


  # === get_from_list

  choices = ['a', 'b', 'c']

  def test_get_fl_default(self):

    with mock.patch('mlstocks.common.input.get_input', return_value=''):
      assert input.get_from_list(self.choices, 'title', 'prompt', default=1) == 'b'


  def test_get_fl(self):

    for i, v in enumerate(self.choices):
      with mock.patch('mlstocks.common.input.get_input', return_value=str(i)):
        assert input.get_from_list(self.choices, 'title', 'prompt', default=i) == self.choices[i]

    return True

  def test_get_fl_gt_1(self):
    global invocation_count
    invocation_count = 0

    with mock.patch('mlstocks.common.input.get_input', side_effect=fls):
      assert input.get_from_list(self.choices, 'title', 'prompt', default=1) == 'b'


  def test_get_fl_exc(self):

    for exc in (KeyboardInterrupt, EOFError, SystemExit):
      with mock.patch('mlstocks.common.input.get_input', mock.MagicMock(side_effect=exc)):
        try:
          input.get_from_list(self.choices, 'title', 'prompt', default=1)
        except SystemExit:
          assert True
    return True


# if __name__ == '__main__':
#   TestCommonInput().test_get_fl_gt_1()
