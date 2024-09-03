import flask
import werkzeug
from webargs import flaskparser
from flask_apispec import utils


class Wrapper:
    """Apply annotations to a view function.

    :param func: View function to wrap
    :param instance: Optional instance or parent
    """

    def __init__(self, func, instance=None):
        self.func = func
        self.instance = instance

    def __call__(self, *args, **kwargs):
        response = self.call_view(*args, **kwargs)
        if isinstance(response, werkzeug.Response):
            return response
        rv, status_code, headers = unpack(response)
        mv = self.marshal_result(rv, status_code)
        response = packed(mv, status_code, headers)
        return flask.current_app.make_response(response)

    def call_view(self, *args, **kwargs):
        config = flask.current_app.config
        parser = config.get('APISPEC_WEBARGS_PARSER', flaskparser.parser)
        annotation = utils.resolve_annotations(self.func, 'args', self.instance)
        if annotation.apply is not False:
            for option in annotation.options:
                schema = utils.resolve_schema(option['argmap'], request=flask.request)
                parsed_args = parser.parse(schema, **option['kwargs'])
                args, kwargs = parser._update_args_kwargs(args, kwargs, parsed_args, option['as_kwargs'])

        return self.func(*args, **kwargs)

    def marshal_result(self, result, status_code):
        config = flask.current_app.config
        format_response = config.get('APISPEC_FORMAT_RESPONSE', flask.jsonify) or identity
        annotation = utils.resolve_annotations(self.func, 'schemas', self.instance)
        schemas = utils.merge_recursive(annotation.options)
        schema = schemas.get(status_code, schemas.get('default'))
        if schema and annotation.apply is not False:
            schema = utils.resolve_schema(schema['schema'], request=flask.request)
            output = schema.dump(result)
        else:
            output = result

        return format_response(output)  # type: Response


def identity(value):
    return value


def unpack(resp):
    data = headers = None
    status_code = 200
    if isinstance(resp, tuple):
        data = resp[0]
        len_resp = len(resp)
        if len_resp == 3:
            status_code, headers = resp[1:]
        elif len_resp == 2:
            if isinstance(resp[1], (werkzeug.datastructures.Headers, dict, tuple, list)):
                headers = resp[1]
            else:
                status_code = resp[1]
    else:
        data = resp
    return data, status_code, headers


def packed(data, status_code, headers):
    resp = (data, )
    if status_code:
        resp += (status_code, )
    if headers:
        resp += (headers, )
    return resp
