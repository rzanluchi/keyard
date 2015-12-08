# -*- coding: utf-8 -*-
import falcon
import falcon.testing
import json

from keyard import app
from keyard.app.utils import prepare_app


class TestIntegrationKeyardResource(falcon.testing.TestBase):

    def before(self):
        self.resource = app.KeyardResource()
        self.api.add_route('/keyard', self.resource)
        prepare_app(self.api)

    def tearDown(self):
        self.resource.api.store.store = {}

    def test_get(self):
        self.resource.api.register('web', '1.0', 'localhost:8080')
        body = self.simulate_request('keyard',
                                     query_string="service_name=web")
        parsed_body = json.loads(body[0])

        self.assertEqual(self.srmock.status, falcon.HTTP_200)
        self.assertEqual(parsed_body.get('result'), ['localhost:8080'])

    def test_get_with_version(self):
        self.resource.api.register('web', '1.0', 'localhost:9090')
        body = self.simulate_request(
            'keyard', query_string="service_name=web&version=1.0")
        parsed_body = json.loads(body[0])

        self.assertEqual(self.srmock.status, falcon.HTTP_200)
        self.assertEqual(parsed_body.get('result'), ['localhost:9090'])

    def test_get_with_load_balancer(self):
        self.resource.api.register('web', '1.0', 'localhost:9090')
        body = self.simulate_request(
            'keyard',
            query_string="service_name=web&load_balancer_strategy=random")
        parsed_body = json.loads(body[0])

        self.assertEqual(self.srmock.status, falcon.HTTP_200)
        self.assertEqual(parsed_body.get('result'), 'localhost:9090')

    def test_bad_get(self):
        body = self.simulate_request('keyard')
        parsed_body = json.loads(body[0])

        self.assertEqual(self.srmock.status, falcon.HTTP_400)
        self.assertTrue('description' in parsed_body, parsed_body)

    def test_post(self):
        self.simulate_request(
            'keyard', method="POST",
            body=json.dumps({'service_name': 'web', 'version': '1.0',
                             'location': 'localhost:8888'}))

        self.assertEqual(self.srmock.status, falcon.HTTP_201)
        self.assertEqual(self.resource.api.get_service('web'),
                         ['localhost:8888'])

    def test_bad_post(self):
        body = self.simulate_request(
            'keyard', method="POST",
            body=json.dumps({'service_name': 'web', 'version': '1.0'}))
        parsed_body = json.loads(body[0])

        self.assertEqual(self.srmock.status, falcon.HTTP_400)
        self.assertTrue('description' in parsed_body, parsed_body)

    def test_put(self):
        self.simulate_request(
            'keyard', method="PUT",
            body=json.dumps({'service_name': 'web', 'version': '1.0',
                             'location': 'localhost:8888'}))

        self.assertEqual(self.srmock.status, falcon.HTTP_200)
        self.assertEqual(self.resource.api.get_service('web'),
                         ['localhost:8888'])

    def test_bad_put(self):
        body = self.simulate_request(
            'keyard', method="PUT",
            body=json.dumps({'service_name': 'web', 'version': '1.0'}))
        parsed_body = json.loads(body[0])

        self.assertEqual(self.srmock.status, falcon.HTTP_400)
        self.assertTrue('description' in parsed_body, parsed_body)

    def test_delete(self):
        self.resource.api.register('web', '1.0', 'localhost:8080')
        self.simulate_request(
            'keyard', method="DELETE",
            body=json.dumps({'service_name': 'web', 'version': '1.0',
                             'location': 'localhost:8080'}))

        self.assertEqual(self.srmock.status, falcon.HTTP_200)
        self.assertEqual(self.resource.api.store.store, {})

    def test_bad_delete(self):
        body = self.simulate_request(
            'keyard', method="DELETE",
            body=json.dumps({'service_name': 'web', 'version': '1.0'}))
        parsed_body = json.loads(body[0])

        self.assertEqual(self.srmock.status, falcon.HTTP_400)
        self.assertTrue('description' in parsed_body, parsed_body)
