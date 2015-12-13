import json


class Config(object):
    defaults = {
        'store_type': 'simple'
    }

    def __init__(self):
        self.config = self.defaults

    def load_file(self, filename):
        with open(filename) as f:
            self.config = json.loads(f.read())

    def get_config(self, section):
        return self.config.get(section, {})


config = Config()
