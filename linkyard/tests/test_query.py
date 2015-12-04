# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, '.')
import mock

from linkyard import store
from linkyard.query import StoreQuery


class TestQueryStore(object):

    def test_get_service_locations(self):
        query = StoreQuery(store=mock.MagicMock())
        query.get_service_locations('web', '1.0')
        query.store.get_key.assert_called_with('web', '1.0', None)


class TestQueryStoreIntegrationMemory(object):

    def test_get_service_locations(self):
        query = StoreQuery(store=store.MemoryStore())
        query.store.set_key('web', '1.0', 'localhost:42')
        assert query.get_service_locations('web', '1.0') == ['localhost:42']

    def test_get_service_locations_multiple(self):
        query = StoreQuery(store=store.MemoryStore())
        query.store.set_key('web', '1.0', 'localhost:42')
        query.store.set_key('web', '1.0', 'localhost:43')
        assert sorted(query.get_service_locations('web', '1.0')) == \
            sorted(['localhost:42', 'localhost:43'])
