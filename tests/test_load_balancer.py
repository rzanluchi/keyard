# -*- coding: utf-8 -*-
import mock

from keyard import load_balancer


class TestLoadBalancers(object):

    @mock.patch('keyard.load_balancer.random')
    def test_random_load_balancer(self, mock_random):
        mock_random.randint.return_value = 1
        values_list = ['localhost:27', 'localhost:7777']
        assert load_balancer.random_choice(values_list) == 'localhost:7777'
