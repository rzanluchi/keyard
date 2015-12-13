# -*- coding: utf-8 -*-
import mock

from keyard import api
from keyard import store


class TestAPI(object):

    def setup_method(self, method):
        self.api = api.API()
        self.api.store = mock.MagicMock()
        self.api.query = mock.MagicMock()
        self.api.commands = mock.MagicMock()

    @mock.patch('keyard.api.store_factory')
    def test_store_setup(self, store_mock):
        self.api = api.API()
        store_mock.assert_called_with('simple')

    def test_api_with_config(self):
        self.api = api.API()
        assert isinstance(self.api.store, store.MemoryStore)

    def test_register(self):
        self.api.register('webapp', '0.1.0', '127.0.0.1:9091')
        self.api.commands.register.assert_called_with(
            'webapp', '0.1.0', '127.0.0.1:9091')

    def test_unregister(self):
        self.api.unregister('webapp', '0.1.0', '127.0.0.1:9091')
        self.api.commands.unregister.assert_called_with(
            'webapp', '0.1.0', '127.0.0.1:9091')

    def test_health_check(self):
        self.api.health_check('webapp', '0.1.0', '127.0.0.1:9091')
        self.api.commands.health_check.assert_called_with(
            'webapp', '0.1.0', '127.0.0.1:9091')

    def test_get_service_with_service_name(self):
        self.api.get_service("webapp")
        self.api.query.get_service.assert_called_with('webapp', None)
