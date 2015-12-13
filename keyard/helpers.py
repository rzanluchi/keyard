import ConfigParser


class Config(object):
    defaults = {
        'store_type': 'simple'
    }

    def __init__(self):
        self.config_parser = ConfigParser.ConfigParser()
        self.config = self.defaults

    def load_file(self, filename):
        self.config = self.config_parser.read(filename)

    def get_config(self, section):
        return self.config.get(section, {})


config = Config()
