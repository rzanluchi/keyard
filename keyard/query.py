# -*- coding: utf-8 -*-


class StoreQuery(object):
    """Query class to interact with the store.
    """
    def __init__(self, store):
        self.store = store

    def get_service(self, service_name, version=None, location=None):
        return self.store.get_key(service_name, version, location)
