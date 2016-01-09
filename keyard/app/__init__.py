# -*- coding: utf-8 -*-
import falcon

from keyard.app import resource
from keyard.app.utils import prepare_app
from keyard.app.middlewares import requireJSON


def create_app():
    """Method for creating the default app with keyard route"""
    app = falcon.API(middleware=[requireJSON()])
    keyard = resource.KeyardResource()
    app.add_route('/keyard', keyard)
    prepare_app(app)
    return app
