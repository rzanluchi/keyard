# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, '.')
from linkyard import store


class TestEtcdStore(object):

    def setup_class(self):
        self.store = store.EtcdStore('127.0.0.1', port=2379,
                                     base_path="services_test")

    def test_get_key(self):
        print self.store.set_key('registry', 'localhost:2747')
        assert self.store.get_services_keys('/services') == ['registry']
