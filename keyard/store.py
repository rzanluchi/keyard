# -*- coding: utf-8 -*-
from etcd.client import Client


class EtcdStore(object):
    """Adapter class for etcd api

    We will store the services in folders at etcd separated by service_name
    version and locaion
    /services/{service_name}/{version}/{location} = {location}
    So that way we can list all different locations for the same service and
    utilize the etcd ttl to expire keys.

    Versions, if not provided, will be 1.0 by default when setting values
    """

    def __init__(self, host="127.0.0.1", base_path="/services",
                 **kwargs):
        self._connect(host, **kwargs)
        self.base_path = base_path

    def _connect(self, etcd_location, **kwargs):
        self.connection = Client(host=etcd_location, **kwargs)

    def get_key(self, service_name, version, location):
        key = self._build_path(service_name, version, location)
        items = self.connection.read(key, recursive=True)
        return [item.value for item in items.children]

    def set_key(self, service_name, version, location, ttl=None):
        assert location
        if not version:
            version = '1.0'
        key = self._build_path(service_name, version, location)
        return bool(self.connection.set(key, location, ttl=ttl))

    def delete_key(self, service_name, version, location):
        "version and location cannot be None"
        assert version
        assert location
        key = self._build_path(service_name, version, location)
        return bool(self.connection.delete(key))

    def _build_path(self, service_name, version, location):
        "Builds the query path for the value in the etcd"
        assert service_name  # service_name is the minimum requirement
        key = "{0}/{1}".format(self.base_path, service_name)
        if version:
            key = "{0}/{1}".format(key, version)
            if location:
                key = "{0}/{1}".format(key, location)

        return key

    def _extract_key(self, path):
        "Removes Base Path of the key"
        return path.split("{0}/".format(self.base_path)).pop()


class MemoryStore(object):
    """Adapter class for in memory store

    Will Store keys composing service_name, version and location to allow
    multiple locations to the same service.
    """
    def __init__(self, **kwargs):
        self.store = {}

    def get_key(self, service_name, version, location):
        keys = self.get_services_keys(service_name, version, location)
        return [self.store[key] for key in keys]

    def set_key(self, service_name, version, location, **kwargs):
        """Accepts **kwargs to be compatible with etcd store that accepts
        ttl parameter"""
        assert location
        if not version:
            version = '1.0'
        key = self._build_path(service_name, version, location)
        self.store[key] = location
        return True

    def delete_key(self, service_name, version, location):
        "version and location cannot be None"
        assert version
        assert location
        key = self._build_path(service_name, version, location)
        if key in self.store:
            del self.store[key]
            return True
        return False

    def get_services_keys(self, service_name, version, location):
        "not sure if I will use it now"
        key = self._build_path(service_name, version, location)
        return filter(lambda k: k.startswith(key), self.store.keys())

    def _build_path(self, service_name, version, location):
        "Builds the key to use at store"
        assert service_name  # service_name is the minimum requirement
        key = service_name
        if version:
            key = "{0}/{1}".format(key, version)
            if location:
                key = "{0}/{1}".format(key, location)

        return key


def store_factory(mode="simple"):
    if mode == "simple":
        return MemoryStore
    elif mode == "etcd":
        return EtcdStore
    else:
        return None
