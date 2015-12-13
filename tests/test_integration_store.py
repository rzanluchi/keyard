# -*- coding: utf-8 -*-
import pytest

from keyard import store
from keyard import testutils


@pytest.mark.skipif(not testutils.etcd_is_available(), reason="etcd is missing")
class TestEtcdStore(object):

    def setup_class(self):
        self.store = store.EtcdStore(host='127.0.0.1', port=2379,
                                     base_path="/services_test")

    def teardown_method(self, method):
        self.store.connection.delete('/services_test', recursive=True)

    def test_get_key(self):
        self.store.set_key('registry', '1.0', 'localhost:2747')
        assert self.store.get_key('registry', None, None) == ['localhost:2747']

    def test_get_key_multiple_locations(self):
        self.store.set_key('registry', '1.0', 'localhost:2747')
        self.store.set_key('registry', '1.0', 'localhost:2748')
        assert self.store.get_key('registry', None, None) == \
            ['localhost:2747', 'localhost:2748']

    def test_set_key(self):
        assert self.store.set_key('registry', '1.0', 'localhost:2747')
        assert self.store.get_key('registry', None, None) == ['localhost:2747']

    def test_delete_key(self):
        assert self.store.set_key('registry', '1.0', 'localhost:2747')
        assert self.store.delete_key('registry', '1.0', 'localhost:2747')
