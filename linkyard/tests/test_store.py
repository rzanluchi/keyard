# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, '.')
import mock
from linkyard import store



class TestEtcdStore(object):

    @mock.patch('linkyard.store.EtcdStore.connect')
    def setup_class(self, mock):
        self.store = store.EtcdStore('127.0.0.1')

    @mock.patch('linkyard.store.EtcdStore.connect')
    def test_connect_called(self, mock):
        local_store = store.EtcdStore('127.0.0.1')
        local_store.connect.assert_called_with('127.0.0.1')

    def test_get_key(self):
        magic_mock = mock.MagicMock()
        magic_mock_node = mock.NonCallableMock(
            **{'node.value': 'localhost:7088'})
        magic_mock.node.get.return_value = magic_mock_node
        self.store.connection = magic_mock
        assert self.store.get_key('registry') == 'localhost:7088'
        self.store.connection.node.get.assert_called_with('registry')

    def test_set_key(self):
        magic_mock = mock.MagicMock()
        magic_mock.node.set.return_value = True
        self.store.connection = magic_mock
        assert self.store.set_key('registry', 'localhost:2747') == True
        self.store.connection.node.set.assert_called_with(
            'registry', 'localhost:2747', ttl=None)

    def test_delete_key(self):
        magic_mock = mock.MagicMock()
        magic_mock.node.delete.return_value = True
        self.store.connection = magic_mock
        assert self.store.delete_key('registry') == True
        self.store.connection.node.delete.assert_called_with('registry')

    def test_append_to_key(self):
        magic_mock = mock.MagicMock()
        magic_mock.node.set.return_value = True
        magic_mock_node = mock.NonCallableMock(
            **{'node.value': 'localhost:7088'})
        magic_mock.node.get.return_value = magic_mock_node
        self.store.connection = magic_mock
        assert self.store.append_to_key('registry', '127.0.0.1:8088') == True
        self.store.connection.node.get.assert_called_with('registry')
        self.store.connection.node.set.assert_called_with('registry',
            ['localhost:7088', '127.0.0.1:8088'], ttl=None)


class TestMemoryStore(object):

    def test_set_key(self):
        local_store = store.MemoryStore()
        local_store.set_key('load_balancer', 'localhost:6666')
        assert local_store.store['load_balancer']
        assert local_store.store['load_balancer'] == 'localhost:6666'

    def test_get_key(self):
        local_store = store.MemoryStore()
        local_store.store['registry'] = 'localhost:8888'
        assert local_store.get_key('registry') == 'localhost:8888'

    def test_delete_key(self):
        local_store = store.MemoryStore()
        local_store.store['registry'] = 'localhost:8888'
        local_store.delete_key('registry')
        assert local_store.store == {}

    def test_append_to_key(self):
        local_store = store.MemoryStore()
        local_store.store['registry'] = 'localhost:8888'
        local_store.append_to_key('registry', 'localhost:57')
        assert local_store.store['registry'] == \
            ['localhost:8888', 'localhost:57']
