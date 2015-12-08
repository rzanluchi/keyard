# -*- coding: utf-8 -*-
import random


def random_choice(choices_list):
    return choices_list[random.randint(0, len(choices_list)-1)]


def load_balancer_factory(strategy='random'):
    """factory that defines which load balancer strategy choose"""
    return available_load_balancers.get(strategy, random_choice)


available_load_balancers = {
    'random': random_choice
}
