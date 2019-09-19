from __future__ import print_function
from .abstract import Config
from .errors import ConfigValueError


class Config_OandAAPI(Config):
    #
    # The default environment variable that points to the location of the v20
    # configuration file
    #
    DEFAULT_ENV = "OA_CONF"

    #
    # The default path for the v20 configuration file
    #
    DEFAULT_PATH = "~/.oa.conf"

    def __init__(self):
        """
        Initialize an empty Config object
        """
        self.hostname = None
        self.streaming_hostname = None
        self.port = 443
        self.ssl = True
        self.token = None
        self.username = None
        self.accounts = []
        self.active_account = None
        self.path = None
        self.datetime_format = "RFC3339"

    def __str__(self):
        """
        Create the string (YAML) representaion of the Config instance
        """

        s = super(Config_OandAAPI, self).__str__()
        s = ""
        s += "hostname: {}\n".format(self.hostname)
        s += "streaming_hostname: {}\n".format(self.streaming_hostname)
        s += "port: {}\n".format(self.port)
        s += "ssl: {}\n".format(str(self.ssl).lower())
        s += "token: {}\n".format(self.token)
        s += "username: {}\n".format(self.username)
        s += "datetime_format: {}\n".format(self.datetime_format)
        s += "accounts:\n"
        for a in self.accounts:
            s += "- {}\n".format(a)
        s += "active_account: {}".format(self.active_account)

        return s

    # def load(self, path):
    #     """
    #     Load the YAML config representation from a file into the Config instance
    #
    #     Args:
    #         path: The location to read the config YAML from
    #     """
    #
    #     self.path = path
    #
    #     try:
    #         with open(os.path.expanduser(path)) as f:
    #             y = yaml.safe_load(f)
    #             self.hostname = y.get("hostname", self.hostname)
    #             self.streaming_hostname = y.get(
    #                 "streaming_hostname", self.streaming_hostname
    #             )
    #             self.port = y.get("port", self.port)
    #             self.ssl = y.get("ssl", self.ssl)
    #             self.username = y.get("username", self.username)
    #             self.token = y.get("token", self.token)
    #             self.accounts = y.get("accounts", self.accounts)
    #             self.active_account = y.get(
    #                 "active_account", self.active_account
    #             )
    #             self.datetime_format = y.get("datetime_format", self.datetime_format)
    #     except Exception as exc:
    #         raise ConfigPathError(path)

    def validate(self):
        """
        Ensure that the Config instance is valid
        """

        if self.hostname is None:
            raise ConfigValueError("hostname")
        if self.streaming_hostname is None:
            raise ConfigValueError("streaming_hostname")
        if self.port is None:
            raise ConfigValueError("port")
        if self.ssl is None:
            raise ConfigValueError("ssl")
        if self.username is None:
            raise ConfigValueError("username")
        if self.token is None:
            raise ConfigValueError("token")
        if self.accounts is None:
            raise ConfigValueError("accounts")
        if self.active_account is None:
            raise ConfigValueError("active_account")
        if self.datetime_format is None:
            raise ConfigValueError("datetime_format")

    # def update_from_input(self):
    #     """
    #     Populate the configuration instance by interacting with the user using
    #     prompts
    #     """
    #
    #     environments = [
    #         "fxtrade",
    #         "fxpractice"
    #     ]
    #
    #     hostnames = [
    #         "api-fxtrade.oanda.com",
    #         "api-fxpractice.oanda.com"
    #     ]
    #
    #     streaming_hostnames = [
    #         "stream-fxtrade.oanda.com",
    #         "stream-fxpractice.oanda.com"
    #     ]
    #
    #     index = 0
    #
    #     try:
    #         index = hostnames.index(self.hostname)
    #     except:
    #         pass
    #
    #     environment = input.get_from_list(
    #         environments,
    #         "Available environments:",
    #         "Select environment",
    #         index
    #     )
    #
    #     index = environments.index(environment)
    #
    #     self.hostname = hostnames[index]
    #     self.streaming_hostname = streaming_hostnames[index]
    #
    #     print("> API host selected is: {}".format(self.hostname))
    #     print("> Streaming host selected is: {}".format(self.streaming_hostname))
    #     print("")
    #
    #     self.username = input.get_string("Enter username", self.username)
    #
    #     print("> username is: {}".format(self.username))
    #     print("")
    #
    #     self.token = input.get_string("Enter personal access token", self.token)
    #
    #     print("> Using personal access token: {}".format(self.token))
    #
    #     ctx = v20.Context(
    #         self.hostname,
    #         self.port,
    #         self.ssl
    #     )
    #
    #     ctx.set_token(self.token)
    #
    #     ctx_streaming = v20.Context(
    #         self.streaming_hostname,
    #         self.port,
    #         self.ssl
    #     )
    #
    #     ctx_streaming.set_token(self.token)
    #
    #     response = ctx.account.list()
    #
    #     if response.status != 200:
    #         print(response)
    #         sys.exit()
    #
    #     self.accounts = [
    #         account.id for account in response.body.get("accounts")
    #     ]
    #
    #     self.accounts.sort()
    #
    #     if len(self.accounts) == 0:
    #         print("No Accounts available")
    #         sys.exit()
    #
    #     index = 0
    #
    #     try:
    #         index = self.accounts.index(self.active_account)
    #     except:
    #         pass
    #
    #     print("")
    #
    #     self.active_account = input.get_from_list(
    #         self.accounts,
    #         "Available Accounts:",
    #         "Select Active Account",
    #         index
    #     )
    #
    #     print("> Active Account is: {}".format(self.active_account))
    #     print("")
    #
    #     time_formats = ["RFC3339", "UNIX"]
    #
    #     index = 0
    #
    #     try:
    #         index = time_formats.index(self.datetime_format)
    #     except:
    #         pass
    #
    #     self.datetime_format = input.get_from_list(
    #         time_formats,
    #         "Available Time Formats:",
    #         "Select Time Format",
    #         index
    #     )

    @classmethod
    def make(self, path):
        """
        Create a Config instance, load its state from the provided path and
        ensure that it is valid.

        Args:
            path: The location of the configuration file
        """
        config = Config_OandAAPI()
        config.load(path)
        config.validate()
        return config
