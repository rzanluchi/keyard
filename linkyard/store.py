# -*- coding: utf-8 -*-
from etcd.client import Client


class EtcdStore(object):
    """Adapter class for etcd api
    """

    def __init__(self, etcd_location="127.0.0.1", base_path="/services",
                 **kwargs):
        self.connect(etcd_location, **kwargs)
        self.base_path = base_path

    def connect(self, etcd_location, **kwargs):
        self.connection = Client(host=etcd_location, **kwargs)

    def get_key(self, key):
        item = self.connection.get(self._build_path(key))
        return item.value

    def set_key(self, key, value, ttl=None):
        return self.connection.set(self._build_path(key), value, ttl=ttl)

    def delete_key(self, key):
        return self.connection.delete(self._build_path(key))

    def get_services_keys(self, key):
        nodes = self.connection.read(key, recursive=True)
        return [self._extract_key(node.key) for node in nodes.children]

    def _build_path(self, path):
        return "{0}/{1}".format(self.base_path, path)

    def _extract_key(self, path):
        return path.split("{0}/".format(self.base_path)).pop()


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

    def get_services_keys(self):
        return self.store.keys()


def store_factory(mode="simple"):
    if mode == "simple":
        return MemoryStore
    elif mode == "etcd":
        return EtcdStore
    else:
        return None
