from __future__ import print_function

import os
import re
from abc import ABCMeta, abstractmethod
from importlib import import_module

import yaml

from .errors import ConfigPathError


class Config(object, metaclass=ABCMeta):
    """
    The Config object encapsulates all of the configuration required to create
    a v20 API context and configure it to work with a specific Account.

    Using the Config object enables the scripts to exist without many command
    line arguments (host, token, accountID, etc)
    """
    #
    # The default environment variable that points to the location of the v20
    # configuration file
    #
    DEFAULT_ENV = "MLS_CONF"

    #
    # The default path for the v20 configuration file
    #
    DEFAULT_PATH = "~/.mls.conf"

    @classmethod
    def default_config_path(self):
        """
        Calculate the default configuration file path.

        The default is first selected to be the contents of the V20_CONF
        environment variable, followed by the default path ~/.v20.conf
        """

        return os.environ.get(self.DEFAULT_ENV, self.DEFAULT_PATH)

    # @abc.abstractmethod
    # def __init__(self):
    #     """
    #     Initialize an empty Config object
    #     """
    #     pass

    def __str__(self):
        """
        Create the string (YAML) representaion of the Config instance
        """

        s = ""
        for a, v in self.__dict__.items():
            s += "{}: {}\n".format(a, str(v))

        return s

    def dump(self, path):
        """
        Dump the YAML representation of the Config instance to a file.

        Args:
            path: The location to write the config YAML
        """

        path = os.path.expanduser(path)

        with open(path, "w") as f:
            print(str(self), file=f)

    def load(self, path):
        """
        Load the YAML config representation from a file into the Config instance

        Args:
            path: The location to read the config YAML from
        """

        self.path = path

        try:
            with open(os.path.expanduser(path)) as f:
                y = yaml.safe_load(f)
                for k, v in y.items():
                    if v is None:
                        v = getattr(self, k)
                    setattr(self, k, v)
        except:
            raise ConfigPathError(path)

    NAMESPACE = '.'.join(__name__.split('.')[0:-1])

    @classmethod
    def _unsupported(cls, _class_name):
        return '{} is not one of our supported Configs!'.format(_class_name)

    @classmethod
    def get_module_class(self, **kwargs):
        config = kwargs.get('config', 'Config')
        translations = {
            # '2019-08': '2019_08.Migration201908',
            # '2019_08': '2019_08.Migration201908',
            # '201908':  '2019_08.Migration201908',
        }
        _class_name = translations.get(config, config)
        if '.' in _class_name:
            _module_name, _class_name = _class_name.rsplit('.', 1)
        else:
            _module_name = _class_name.lower()
            # _class_name = _class_name.capitalize()
        _class_name = _class_name.replace('-', '_')
        if re.match('^[0-9]', _class_name):
            _class_name = 'Config_' + _class_name
            if '.' not in _class_name:
                _module_name = _class_name.lower()
        return _module_name, _class_name

    @classmethod
    def klass(self, *args, **kwargs):
        _module_name, _class_name = self.get_module_class(**kwargs)
        _package = '.'.join(__name__.split('.')[:-1])
        try:
            _module = import_module('.' + _module_name, package=_package)
            _class = getattr(_module, _class_name)

            if not issubclass(_class, Config):
                raise ImportError("{} You are welcome to send in the request for it!"
                                  .format(Config._unsupported('Class ' + _class.__name__)))

            return _class
        except ModuleNotFoundError as exc:
            path = os.path.join(os.path.dirname(__file__), _module_name + '.py')
            if os.path.exists(path):
                raise ImportError('{} exists but importing it failed!'
                                  ' Please check the syntax ...'.format(path))
            raise ImportError(Config._unsupported(_class_name))
        except AttributeError as exc:
            raise ImportError('{} Available classes: {}\n{}'.format(
                Config._unsupported(_class_name),
                [cls.__name__ for nam, cls in _module.__dict__.items()
                    if type(cls) == type(Config)],
                str(exc)))

    @classmethod
    def instantiate(self, *args, **kwargs):
        return self.klass(*args, **kwargs)()

    @classmethod
    def factory(self, *args, **kwargs):
        return Config.instantiate(*args, **kwargs)

    @classmethod
    def manufacture(self, class_name, *args, **kwargs):
        kwargs['config'] = class_name
        return Config.instantiate(*args, **kwargs)

    @abstractmethod
    def make(self, path):
        pass
