# -*- coding: utf-8 -*-
import falcon
from keyard.app import errors


def prepare_app(app):
    """Prepare method to help build falcon api instance"""
    _add_error_handlers(app)


def _add_error_handlers(app):
    """Method to add error handling"""
    app.add_error_handler(Exception, errors.handle_default_errors)
    app.add_error_handler(falcon.HTTPError, errors.handle_falcon_errors)
    app.add_error_handler(AssertionError, errors.handle_assertion_errors)
