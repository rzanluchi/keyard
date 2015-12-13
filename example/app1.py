
# -*- coding: utf-8 -*-
import falcon
import requests
import json


class App1(object):

    def on_get(self, req, resp):
        app2_host = requests.get('http://127.0.0.1:8000/keyard?'
                                 'service_name=app2&'
                                 'load_balancer_strategy=random').text
        app2_host = json.loads(app2_host)
        app2_value = requests.get("http://{0}/app2".format(app2_host['result']))
        resp.body = "Hello {0}".format(app2_value.text)


app = falcon.API()
app.add_route('/app1', App1())
