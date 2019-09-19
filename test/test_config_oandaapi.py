import copy
import io
import os
from tempfile import mktemp

import mock
import yaml
from pytest import fixture

from mlstocks.config.errors import ConfigPathError, ConfigValueError
from mlstocks.config.oandaapi import Config_OandAAPI


@fixture
def oanda_yaml():
  return {
    'hostname': 'hostname',
    'streaming_hostname': 'hostname',
    'port': 443,
    'ssl': True,
    'token': 'token',
    'username': 'username',
    'datetime_format': 'RFC3339',
    'accounts':
      [ 'account' ],
    'active_account': 'account',
  }


class TestConfigOandAAPI():

  def test_instance(self):
    assert Config_OandAAPI()


  def test_default_config_path(self):
    assert Config_OandAAPI.default_config_path() == '~/.oa.conf'


  def test_env_config_path(self):
    path = mktemp()
    os.environ['OA_CONF'] = path
    assert Config_OandAAPI.default_config_path() == path


  def test_namespace(self):
    assert Config_OandAAPI.NAMESPACE == 'mlstocks.config'


  def test_get_module_class(self):
    _module_name, _class_name = Config_OandAAPI.get_module_class(config='oandaapi.OandAAPI')
    print('_module_name={}'.format(_module_name))
    assert _class_name == 'OandAAPI'
    assert _module_name == 'oandaapi'


  def test_str(self):
    coaa = Config_OandAAPI()
    coaa.accounts = ['account']
    assert str(coaa) == """hostname: None
streaming_hostname: None
port: 443
ssl: true
token: None
username: None
datetime_format: RFC3339
accounts:
- account
active_account: None"""

  def test_load_cpe(self):
    try:
      coaa = Config_OandAAPI()
      coaa.load('/path')
    except ConfigPathError as cpe:
      assert str(cpe) == "Config file '/path' could not be loaded."


  def test_load(self, oanda_yaml):
    new_yaml = oanda_yaml
    new_yaml['active_account'] = None
    with mock.patch('yaml.load', return_value=new_yaml):
      with mock.patch('builtins.open', return_value=io.StringIO()):
        coaa = Config_OandAAPI()
        coaa.load('/path')
        # assert str(coaa) == yaml.dump(oanda_yaml)
        assert str(coaa) == """hostname: hostname
streaming_hostname: hostname
port: 443
ssl: true
token: token
username: username
datetime_format: RFC3339
accounts:
- account
active_account: None"""


  def test_validate(self, oanda_yaml):
    with mock.patch('yaml.load', return_value=oanda_yaml):
      with mock.patch('builtins.open', return_value=io.StringIO()):
        coaa = Config_OandAAPI()
        coaa.load('/path')
        for a in oanda_yaml.keys():
          try:
            clon = copy.deepcopy(coaa)
            setattr(clon, a, None)
            clon.validate()
          except ConfigValueError as cve:
            assert "Config is missing value for '{}'.".format(a) == str(cve)


  def test_make_yaml(self, oanda_yaml):
    with mock.patch('yaml.load', return_value=oanda_yaml):
      with mock.patch('builtins.open', return_value=io.StringIO()):
        coaa = Config_OandAAPI.make('/path')
        assert coaa


  def test_dump(self, oanda_yaml):
    coaa = Config_OandAAPI()

    with mock.patch('yaml.load', return_value=oanda_yaml):
      with mock.patch('builtins.open', return_value=io.StringIO()):
        coaa.load('/path')

    coaa.dump('/tmp/oanda.yaml')
    assert os.path.exists('/tmp/oanda.yaml')
    coab = Config_OandAAPI()
    coab.load('/tmp/oanda.yaml')
    assert str(coab) == str(coaa)


  def test_klass_sup(self):
    Config_OandAAPI.klass(config='oandaapi.Config_OandAAPI')


  def test_klass_sup_sub(self):
    with mock.patch('builtins.issubclass', return_value=False):
      try:
        Config_OandAAPI.klass(config='oandaapi.Config_OandAAPI')
      except ImportError as ie:
        assert str(ie) == 'Class Config_OandAAPI is not one of our supported Configs! You are welcome to send in the request for it!'


  def test_klass_sup_path(self):
    with mock.patch('os.path.exists', return_value=True):
      try:
        Config_OandAAPI.klass(config='Fake')
      except ImportError as ie:
        path = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))
        ies = str(ie)
        ies.replace(path, '')
        assert ies.replace(path, '') == '/mlstocks/config/fake.py exists but importing it failed! Please check the syntax ...'


  def test_klass_unsup(self):
    try:
      Config_OandAAPI.klass(config='fake.Fake')
    except ImportError as ie:
      print(str(ie))
      assert str(ie) == 'Fake is not one of our supported Configs!'


  def test_klass_unsup_num(self):
    try:
      Config_OandAAPI.klass(config='config_123.Config_123')
    except ImportError as ie:
      print(str(ie))
      assert str(ie) == 'Config_123 is not one of our supported Configs!'


  def test_instantiate(self):
    Config_OandAAPI.instantiate(config='oandaapi.Config_OandAAPI')


  def test_factory(self):
    Config_OandAAPI.factory(config='oandaapi.Config_OandAAPI')


  def test_manufacture(self):
    Config_OandAAPI.manufacture('oandaapi.Config_OandAAPI')


  def test_make_configpatherror(self):
    try:
      Config_OandAAPI.make('/path')
    except ConfigPathError as cpe:
      assert str(cpe) == "Config file '/path' could not be loaded."

# if __name__ == '__main__':
#   TestConfigOandAAPI().test_manufacture()
  # TestConfigOandAAPI().test_dump({
  #   'hostname': 'hostname',
  #   'streaming_hostname': 'hostname',
  #   'port': 443,
  #   'ssl': True,
  #   'token': 'token',
  #   'username': 'username',
  #   'datetime_format': 'RFC3339',
  #   'accounts':
  #     [ 'account' ],
  #   'active_account': 'account',
  # })
