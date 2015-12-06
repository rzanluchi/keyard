# -*- coding: utf-8 -*-
import falcon
import falcon.testing
import json
import mock

from linkyard import app


class TestLinkyardResource(falcon.testing.TestBase):

    def before(self):
        self.resource = app.LinkyardResource()
        self.resource.api = mock.MagicMock()
        self.api.add_route('/linkyard', self.resource)

    def test_get(self):
        self.resource.api.get_service.return_value = "localhost:8080"
        body = self.simulate_request('linkyard',
                                     query_string="service_name=web")
        parsed_body = json.loads(body[0])

        self.assertEqual(self.srmock.status, falcon.HTTP_200)
        self.assertEqual(parsed_body.get('result'), 'localhost:8080')
        self.resource.api.get_service.assert_called_with('web', None)

    def test_get_with_version(self):
        self.resource.api.get_service.return_value = "localhost:8080"
        body = self.simulate_request(
            'linkyard', query_string="service_name=web&version=1.0")
        parsed_body = json.loads(body[0])

        self.assertEqual(self.srmock.status, falcon.HTTP_200)
        self.assertEqual(parsed_body.get('result'), 'localhost:8080')
        self.resource.api.get_service.assert_called_with('web', '1.0')

    def test_wrong_get(self):
        self.resource.api.get_service.return_value = "localhost:8080"
        body = self.simulate_request('linkyard')
        parsed_body = json.loads(body[0])

        self.assertEqual(self.srmock.status, falcon.HTTP_500)
        self.resource.api.get_service.assert_called_with(None, None)

    def test_post(self):
        self.resource.api.register.return_value = True
        body = self.simulate_request(
            'linkyard', method="POST",
            body=json.dumps({'service_name': 'web', 'version': '1.0',
                             'location': 'localhost:8888'}))

        self.assertEqual(self.srmock.status, falcon.HTTP_201)
        self.resource.api.register.assert_called_with('web', '1.0',
                                                      'localhost:8888')

