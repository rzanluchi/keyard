# -*- coding: utf-8 -*-
from etcd.client import Client


class EtcdStore(object):
    """Adapter class for etcd api
    """
    def __init__(self, etcd_location=""):
        self.connect(etcd_location)

    def connect(self, etcd_location):
        self.connection = Client(etcd_location)

    def get_key(self, key):
        item = self.connection.node.get(key)
        return item.node.value

    def set_key(self, key, value, ttl=None):
        return self.connection.node.set(key, value, ttl=ttl)

    def delete_key(self, key):
        return self.connection.node.delete(key)

    def append_to_key(self, key, value, ttl=None):
        item_value = self.get_key(key)
        if type(item_value) == list:
            item_value.append(item_value)
        else:
            item_value = [item_value, value]
        return self.set_key(key, item_value)


class MemoryStore(object):
    """Adapter class for in memory store
    """
    def __init__(self, **kwargs):
        self.store = {}

    def get_key(self, key):
        return self.store.get(key)

    def set_key(self, key, value, **kwargs):
        self.store[key] = value
        return True

    def delete_key(self, key):
        del self.store[key]

    def append_to_key(self, key, value, **kwargs):
        item_value = self.get_key(key)
        if type(item_value) == list:
            item_value.append(value)
        else:
            item_value = [item_value, value]
        return self.set_key(key, item_value)


def store_factory(mode="simple"):
    if mode == "simple":
        return MemoryStore
    elif mode == "etcd":
        return EtcdStore
    else:
        return None
