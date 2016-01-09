# -*- coding: utf-8 -*-
import falcon
import json

from keyard import api


class KeyardResource(object):

    def __init__(self):
        self.api = api.API()

    def on_get(self, req, resp):
        service_name = req.get_param('service_name')
        version = req.get_param('version')
        load_balancer_strategy = req.get_param('load_balancer_strategy')
        result = self.api.get_service(service_name, version,
                                      load_balancer_strategy)
        resp.status = falcon.HTTP_200
        resp.body = json.dumps({'result': result})

    def on_post(self, req, resp):
        data = json.loads(req.stream.read())
        service_name = data.get('service_name', None)
        version = data.get('version', None)
        location = data.get('location', None)
        self.api.register(service_name, version, location)
        resp.status = falcon.HTTP_200
        resp.body = ''

    def on_put(self, req, resp):
        data = json.loads(req.stream.read())
        service_name = data.get('service_name', None)
        version = data.get('version', None)
        location = data.get('location', None)
        self.api.health_check(service_name, version, location)
        resp.status = falcon.HTTP_200
        resp.body = ''

    def on_delete(self, req, resp):
        data = json.loads(req.stream.read())
        service_name = data.get('service_name', None)
        version = data.get('version', None)
        location = data.get('location', None)
        self.api.unregister(service_name, version, location)
        resp.status = falcon.HTTP_200
        resp.body = ''
