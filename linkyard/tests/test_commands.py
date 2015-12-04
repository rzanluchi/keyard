# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, '.')
import mock

from linkyard import store
from linkyard.commands import StoreCommands


class TestStoreCommands(object):

    def test_register(self):
        commands = StoreCommands(mock.MagicMock())
        commands.register('web', '1.0', 'localhost:42')
        commands.store.set_key.assert_called_with('web', '1.0', 'localhost:42')

    def test_unregister(self):
        commands = StoreCommands(mock.MagicMock())
        commands.unregister('web', '1.0', 'localhost:42')
        commands.store.delete_key.assert_called_with('web', '1.0',
                                                     'localhost:42')

    def test_health_check(self):
        commands = StoreCommands(mock.MagicMock())
        commands.health_check('web', '1.0', 'localhost:42')
        commands.store.set_key.assert_called_with('web', '1.0', 'localhost:42')


class TestStoreCommandsIntegrationMemory(object):

    def test_register(self):
        commands = StoreCommands(store.MemoryStore())
        commands.register('web', '1.0', 'localhost:42')
        assert commands.store.get_key('web', '1.0', 'localhost:42') == \
            ['localhost:42']

    def test_unregister(self):
        commands = StoreCommands(store.MemoryStore())
        commands.unregister('web', '1.0', 'localhost:42')
        assert commands.store.get_key('web', '1.0', 'localhost:42') == []

    def test_health_check(self):
        commands = StoreCommands(store.MemoryStore())
        commands.health_check('web', '1.0', 'localhost:42')
        assert commands.store.get_key('web', '1.0', 'localhost:42') == \
            ['localhost:42']
