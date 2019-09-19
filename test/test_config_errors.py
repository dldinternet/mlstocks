from mlstocks.config.errors import ConfigPathError, ConfigValueError


class TestConfigErrors():

    def test_configpatherror(self):
        try:
            raise ConfigPathError('/path')
        except ConfigPathError as cpe:
            assert cpe.args[0] == '/path'
            assert str(cpe) == "Config file '/path' could not be loaded."

    def test_ConfigValueError(self):
        try:
            raise ConfigValueError('value')
        except ConfigValueError as cve:
            assert cve.value == 'value'
            assert str(cve) == "Config is missing value for 'value'."
