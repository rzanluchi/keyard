# -*- coding: utf-8 -*-
import mock

from keyard import helpers


class TestConfig(object):

    def test_load_config(self):
        config = helpers.Config()
        config_dict = {'section1': {'foo': 'bar'}}
        config.config_parser = mock.MagicMock()
        config.config_parser.read.return_value = config_dict
        config.load_file('/path/to/file.conf')
        assert config.config == config_dict
        config.config_parser.read.assert_called_with('/path/to/file.conf')

    def test_get_config(self):
        config = helpers.Config()
        config.config = {'section1': {'foo': 'bar'}}
        assert config.get_config('section1') == {'foo': 'bar'}

    def test_defaults(self):
        config = helpers.Config()
        assert config.get_config('store_type') == 'simple'
