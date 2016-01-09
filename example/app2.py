# -*- coding: utf-8 -*-
import falcon
import json
import requests


class App2(object):

    def on_get(self, req, resp):
        resp.body = "World"


app = falcon.API()
app.add_route('/app2', App2())
requests.post('http://localhost:8000/keyard', data=json.dumps({
    'service_name': 'app2',
    'version': '1.0',
    'location': 'localhost:8002'
}), headers={'content-type': 'application/json'})
