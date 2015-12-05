# -*- coding: utf-8 -*-
import mock

from linkyard import api


class TestAPI(object):

    def setup_method(self, method):
        self.api = api.API()
        self.api.store = mock.MagicMock()
        self.api.query = mock.MagicMock()
        self.api.commands = mock.MagicMock()

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
