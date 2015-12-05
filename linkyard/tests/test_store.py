# -*- coding: utf-8 -*-
import mock
from linkyard import store


class TestEtcdStore(object):

    @mock.patch('linkyard.store.EtcdStore._connect')
    def setup_class(self, mock):
        self.store = store.EtcdStore('127.0.0.1')

    @mock.patch('linkyard.store.EtcdStore._connect')
    def test_connect_called(self, mock):
        local_store = store.EtcdStore('127.0.0.1')
        local_store._connect.assert_called_with('127.0.0.1')

    def test_get_key_with_service_name(self):
        magic_mock = mock.MagicMock()
        magic_mock_node = mock.NonCallableMock(
            **{'value': 'localhost:7088'})
        magic_mock.get.return_value = magic_mock_node
        self.store.connection = magic_mock
        assert self.store.get_key('registry', None, None) == 'localhost:7088'
        self.store.connection.get.assert_called_with('/services/registry')

    def test_get_key_with_version(self):
        magic_mock = mock.MagicMock()
        magic_mock_node = mock.NonCallableMock(
            **{'value': 'localhost:7088'})
        magic_mock.get.return_value = magic_mock_node
        self.store.connection = magic_mock
        assert self.store.get_key('registry', '1.0', None) == 'localhost:7088'
        self.store.connection.get.assert_called_with('/services/registry/1.0')

    def test_get_key_with_location(self):
        magic_mock = mock.MagicMock()
        magic_mock_node = mock.NonCallableMock(
            **{'value': 'localhost:7088'})
        magic_mock.get.return_value = magic_mock_node
        self.store.connection = magic_mock
        assert self.store.get_key('registry', '1.0', 'localhost:7088') \
            == 'localhost:7088'
        self.store.connection.get.assert_called_with(
            '/services/registry/1.0/localhost:7088')

    def test_set_key(self):
        magic_mock = mock.MagicMock()
        magic_mock.set.return_value = True
        self.store.connection = magic_mock
        assert self.store.set_key('registry', '1.0', 'localhost:2747') is True
        self.store.connection.set.assert_called_with(
            '/services/registry/1.0/localhost:2747', 'localhost:2747', ttl=None)

    def test_delete_key(self):
        magic_mock = mock.MagicMock()
        magic_mock.delete.return_value = True
        self.store.connection = magic_mock
        assert self.store.delete_key('registry', '1.0', 'localhost:48') is True
        self.store.connection.delete.assert_called_with(
            '/services/registry/1.0/localhost:48')


class TestMemoryStore(object):

    def test_set_key(self):
        local_store = store.MemoryStore()
        local_store.set_key('load_balancer', None, 'localhost:6666')
        assert local_store.store['load_balancer/1.0/localhost:6666']
        assert local_store.store['load_balancer/1.0/localhost:6666'] == \
            'localhost:6666'

    def test_get_key(self):
        local_store = store.MemoryStore()
        local_store.store['registry/1.0/localhost:42'] = 'localhost:42'
        assert 'localhost:42' in local_store.get_key('registry', '1.0',
                                                     'localhost:42')

    def test_get_key_without_location(self):
        local_store = store.MemoryStore()
        local_store.store['registry/1.0/localhost:42'] = 'localhost:42'
        local_store.store['registry/1.0/localhost:43'] = 'localhost:43'
        assert sorted(['localhost:42', 'localhost:43']) == sorted(
            local_store.get_key('registry', '1.0', None))

    def test_get_key_without_version(self):
        local_store = store.MemoryStore()
        local_store.store['registry/1.0/localhost:42'] = 'localhost:42'
        local_store.store['registry/1.0/localhost:43'] = 'localhost:43'
        assert sorted(['localhost:42', 'localhost:43']) == sorted(
            local_store.get_key('registry', None, None))

    def test_delete_key(self):
        local_store = store.MemoryStore()
        local_store.store['registry/1.0/localhost:8888'] = 'localhost:8888'
        local_store.delete_key('registry', '1.0', 'localhost:8888')
        assert local_store.store == {}
