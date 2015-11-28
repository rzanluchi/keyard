# -*- coding: utf-8 -*-
import commands
import query
from store import store_factory


class API(object):
    """This class represent all methods that can be exposed for other services
    by either HTTP or RPC.

    This class will be a gateway for command/query methods
    """
    def __init__(self, store_mode="simple", **kwargs):
        self.store = store_factory(store_mode)(**kwargs)
        self.commands = commands.StoreCommands(self.store)
        self.query = query.StoreQuery(self.store)

    def register(self, service_name, location):
        """Endpoint to register a ative service
        Args:
            service_name: will be the name of the serivce
            location: will be the location of that service
        Returns:
            return a boolean with status of the operation in etcd
        """
        return self.commands.register(service_name, location)

    def unregister(self, service_name, location):
        """Endpoint to unregister a ative service
        Args:
            service_name: will be the name of the serivce
            location: will be the location of that service
        Returns:
            return a boolean with status of the operation in etcd
        """
        return self.ommands.unregister(service_name, location)

    def health_check(self, service_name, location):
        """Endpoint to renew the tll of a service in a location
        Args:
            service_name: will be the name of the serivce
            location: will be the location of that service
        Returns:
            return a boolean with status of the operation in etcd
        """
        return self.commands.health_check(service_name, location)

    def get_service_locations(self, service_name):
        """Endpoint to list all available locations by service name
        Args:
            service_name: name of the service
        Returns
            returns a list with all avaiable locations for that service
        """
        return self.query.get_service_locations(service_name)
