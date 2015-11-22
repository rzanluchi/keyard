# -*- coding: utf-8 -*-
from etcd.client import Client


class EtcdStore(object):
    """Adapter class for etcd api
    """
    instance = None

    def __init__(self, etcd_location=""):
        self.connect(etcd_location)

    def connect(self, etcd_location):
        self.connection = Client(etcd_location)

    def get_key(self, key):
        return self.connection.node.get(key)

    def set_key(self, key, value, ttl=None):
        return self.connection.node.set(key, value, ttl=ttl)

    def delete_key(self, key):
        return self.connection.node.delete(key)

    def append_to_key(self, key, value, ttl):
        item = self.get_key(key)
        item_value = item.node.value
        if type(item_value) == list:
            item_value.append(value)
        else:
            item_value = [item_value, value]
        return self.set_key(key, item_value)


store = EtcdStore()
