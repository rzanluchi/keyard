# -*- coding: utf-8 -*-


class StoreCommands(object):
    """Commands class to interact with the store.
    """
    def __init__(self, store):
        self.store = store

    def register(self, service_name, location):
        self.store.append_to_key(service_name, location)

    def unregister(self, service_name, location):
        self.store.delete_key(service_name)

    def health_check(self, service_name, location):
        self.store.set_key(service_name, location)
