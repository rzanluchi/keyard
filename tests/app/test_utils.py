# -*- coding: utf-8 -*-
import mock
import falcon
import falcon.testing

from keyard.app import utils
from keyard.app import errors


class TestUtils(falcon.testing.TestBase):

    @mock.patch('keyard.app.utils._add_error_handlers')
    def test_prepare_app(self, handler_mock):
        app = mock.MagicMock()
        utils.prepare_app(app)
        handler_mock.assert_called_with(app)

    def test_add_error_handlers(self):
        app = mock.MagicMock()
        utils._add_error_handlers(app)
        calls = [mock.call.add_error_handler(Exception,
                                             errors.handle_default_errors),
                 mock.call.add_error_handler(falcon.HTTPError,
                                             errors.handle_falcon_errors),
                 mock.call.add_error_handler(AssertionError,
                                             errors.handle_assertion_errors)]
        app.assert_has_calls(calls)
