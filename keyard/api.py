# -*- coding: utf-8 -*-
import commands
import load_balancer
import query
from keyard.helpers import config
from store import store_factory


class API(object):
    """This class represent all methods that can be exposed for other services
    by either HTTP or RPC.

    This class will be a gateway for command/query methods
    """
    def __init__(self):
        store_type = config.get_config('store_type')
        self.store = store_factory(store_type)(**config.get_config(store_type))
        self.commands = commands.StoreCommands(self.store)
        self.query = query.StoreQuery(self.store)

    def register(self, service_name, version, location):
        """Endpoint to register a ative service
        Args:
            service_name: will be the name of the serivce
            version: will be the version of the service e.g. 1.0
            location: will be the location of that service
        Returns:
            return a boolean with status of the operation in etcd
        """
        return self.commands.register(service_name, version, location)

    def unregister(self, service_name, version, location):
        """Endpoint to unregister a ative service
        Args:
            service_name: will be the name of the serivce
            version: will be the version of the service e.g. 1.0
            location: will be the location of that service
        Returns:
            return a boolean with status of the operation in etcd
        """
        return self.commands.unregister(service_name, version, location)

    def health_check(self, service_name, version, location):
        """Endpoint to renew the tll of a service in a location
        Args:
            service_name: will be the name of the serivce
            version: will be the version of the service e.g. 1.0
            location: will be the location of that service
        Returns:
            return a boolean with status of the operation in etcd
        """
        return self.commands.health_check(service_name, version, location)

    def get_service(self, service_name, version=None,
                    load_balancer_strategy=None):
        """Endpoint to list all available locations by service name
        Args:
            service_name: name of the service
            version: will be the version of the service e.g. 1.0
            load_balancer_strategy: name of the load balancer strategy do apply
                on the results. None will return the whole list to the client
        Returns
            returns a list with all avaiable locations for that service
        """
        locations = self.query.get_service(service_name, version)
        if load_balancer_strategy:
            strategy_func = load_balancer.load_balancer_factory(
                load_balancer_strategy)
            locations = strategy_func(locations)

        return locations
