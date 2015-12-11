import ConfigParser


class Config(object):

    def __init__(self):
        self.config_parser = ConfigParser.ConfigParser()

    def load_file(self, filename):
        self.config = self.config_parser.read(filename)

    def get_config(self, section):
        return self.config[section]


config = Config()
