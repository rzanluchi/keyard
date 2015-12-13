# -*- coding: utf-8 -*-
import falcon
import falcon.testing
import json
import mock

from keyard.app import resource
from keyard.app.utils import prepare_app


class TestKeyardResource(falcon.testing.TestBase):

    def before(self):
        self.resource = resource.KeyardResource()
        self.resource.api = mock.MagicMock()
        self.api.add_route('/keyard', self.resource)
        prepare_app(self.api)

    def test_get(self):
        self.resource.api.get_service.return_value = ["localhost:8080"]
        body = self.simulate_request('keyard',
                                     query_string="service_name=web")
        parsed_body = json.loads(body[0])

        self.assertEqual(self.srmock.status, falcon.HTTP_200)
        self.assertEqual(parsed_body.get('result'), ['localhost:8080'])
        self.resource.api.get_service.assert_called_with('web', None, None)

    def test_get_with_version(self):
        self.resource.api.get_service.return_value = ["localhost:8080"]
        body = self.simulate_request(
            'keyard', query_string="service_name=web&version=1.0")
        parsed_body = json.loads(body[0])

        self.assertEqual(self.srmock.status, falcon.HTTP_200)
        self.assertEqual(parsed_body.get('result'), ['localhost:8080'])
        self.resource.api.get_service.assert_called_with('web', '1.0', None)

    def test_get_with_load_balancer(self):
        self.resource.api.get_service.return_value = "localhost:8080"
        body = self.simulate_request(
            'keyard',
            query_string="service_name=web&load_balancer_strategy=random")
        parsed_body = json.loads(body[0])

        self.assertEqual(self.srmock.status, falcon.HTTP_200)
        self.assertEqual(parsed_body.get('result'), 'localhost:8080')
        self.resource.api.get_service.assert_called_with('web', None, 'random')

    def test_bad_get(self):
        self.resource.api.get_service.return_value = "localhost:8080"
        self.resource.api.get_service.side_effect = AssertionError
        self.simulate_request('keyard')

        self.assertEqual(self.srmock.status, falcon.HTTP_400)
        self.resource.api.get_service.assert_called_with(None, None, None)

    def test_post(self):
        self.resource.api.register.return_value = True
        self.simulate_request(
            'keyard', method="POST",
            body=json.dumps({'service_name': 'web', 'version': '1.0',
                             'location': 'localhost:8888'}))

        self.assertEqual(self.srmock.status, falcon.HTTP_200)
        self.resource.api.register.assert_called_with('web', '1.0',
                                                      'localhost:8888')

    def test_bad_post(self):
        self.resource.api.register.return_value = True
        self.resource.api.register.side_effect = AssertionError
        self.simulate_request(
            'keyard', method="POST",
            body=json.dumps({'service_name': 'web', 'version': '1.0'}))

        self.assertEqual(self.srmock.status, falcon.HTTP_400)
        self.resource.api.register.assert_called_with('web', '1.0', None)

    def test_put(self):
        self.resource.api.health_check.return_value = True
        self.simulate_request(
            'keyard', method="PUT",
            body=json.dumps({'service_name': 'web', 'version': '1.0',
                             'location': 'localhost:8888'}))

        self.assertEqual(self.srmock.status, falcon.HTTP_200)
        self.resource.api.health_check.assert_called_with('web', '1.0',
                                                          'localhost:8888')

    def test_bad_put(self):
        self.resource.api.health_check.return_value = True
        self.resource.api.health_check.side_effect = AssertionError
        self.simulate_request(
            'keyard', method="PUT",
            body=json.dumps({'service_name': 'web', 'version': '1.0'}))

        self.assertEqual(self.srmock.status, falcon.HTTP_400)
        self.resource.api.health_check.assert_called_with('web', '1.0', None)

    def test_delete(self):
        self.resource.api.unregister.return_value = True
        self.simulate_request(
            'keyard', method="DELETE",
            body=json.dumps({'service_name': 'web', 'version': '1.0',
                             'location': 'localhost:8888'}))

        self.assertEqual(self.srmock.status, falcon.HTTP_200)
        self.resource.api.unregister.assert_called_with('web', '1.0',
                                                        'localhost:8888')

    def test_bad_delete(self):
        self.resource.api.unregister.return_value = True
        self.resource.api.unregister.side_effect = AssertionError
        self.simulate_request(
            'keyard', method="DELETE",
            body=json.dumps({'service_name': 'web', 'version': '1.0'}))

        self.assertEqual(self.srmock.status, falcon.HTTP_400)
        self.resource.api.unregister.assert_called_with('web', '1.0', None)
