import falcon


def handle_assertion_errors(ex, req, resp, params):
    description = "Bad Request"
    raise falcon.HTTPBadRequest('Missing parameters',
                                description=description)

def handle_falcon_errors(ex, req, resp, params):
    raise ex

def handle_default_errors(ex, req, resp, params):
    description = str(ex)
    raise falcon.HTTPError(falcon.HTTP_500, 'Server Error',
                           description=description)
