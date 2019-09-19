import os
from tempfile import mktemp

from mlstocks.config.abstract import Config


class TestConfigAbstract():

  def test_instantiate(self):

    try:
      Config()
    except TypeError:
      return True


  def test_default_config_path(self):
    assert Config.default_config_path() == '~/.mls.conf'


  def test_env_config_path(self):
    path = mktemp()
    os.environ['MLS_CONF'] = path
    assert Config.default_config_path() == path


  def test_namespace(self):
    assert Config.NAMESPACE == 'mlstocks.config'


  def test_get_module_class(self):
    _module_name, _class_name = Config.get_module_class()
    print('mod: {}'.format(_module_name))
    assert _class_name == 'Config'
    assert _module_name == 'config'


  def test_get_module_class_num(self):
    _module_name, _class_name = Config.get_module_class(config='config.123')
    print('mod: {}'.format(_module_name))
    assert _class_name == 'Config_123'
    assert _module_name == 'config_123'


# if __name__ == '__main__':
#   TestConfigAbstract().test_get_module_class()
