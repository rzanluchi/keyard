# -*- coding: utf-8 -*-
from keyard import helpers


class TestConfig(object):

    def test_load_config(self):
        config = helpers.Config()
        config.load_file('tests/test_config.json')
        assert config.config == {"store_type": "simple"}

    def test_get_config(self):
        config = helpers.Config()
        config.config = {'section1': {'foo': 'bar'}}
        assert config.get_config('section1') == {'foo': 'bar'}

    def test_defaults(self):
        config = helpers.Config()
        assert config.get_config('store_type') == 'simple'
