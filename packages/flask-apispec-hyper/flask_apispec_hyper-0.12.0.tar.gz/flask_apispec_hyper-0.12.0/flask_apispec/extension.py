import flask
import functools
import types
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin

from flask_apispec.apidoc import ViewConverter, ResourceConverter


class FlaskApiSpec:
    """Flask-apispec extension.

    Usage:

    .. code-block:: python

        app = Flask(__name__)
        app.config.update({
            'APISPEC_SPEC': APISpec(
                title='pets',
                version='v1',
                openapi_version='3.1.0',
                plugins=[MarshmallowPlugin()],
            ),
            'APISPEC_SWAGGER_URL': '/swagger/',
        })
        docs = FlaskApiSpec(app)

        @app.route('/pet/<pet_id>')
        def get_pet(pet_id):
            return Pet.query.filter(Pet.id == pet_id).one()

        docs.register(get_pet)

    :param Flask app: App associated with API documentation
    :param APISpec spec: apispec specification associated with API documentation
    :param bool document_options: Whether or not to include
        OPTIONS requests in the specification
    """

    def __init__(self, app=None, **kwargs):
        self._deferred = []
        self.app = app
        self.view_converter = None
        self.resource_converter = None
        self.spec = None

        if app:
            self.init_app(app, **kwargs)

    def init_app(self, app, spec=None, title=None, version="v1", openapi_version="3.1.0", url_prefix=None, spec_url="/apispec.json", doc_url="/apidocs", document_options=None):
        self.app = app
        self.spec = spec or make_apispec(app.config.get('APISPEC_TITLE', title or app.import_name),
                                 app.config.get('APISPEC_VERSION', version),
                                 app.config.get('APISPEC_OAS_VERSION', openapi_version))
        self.url_prefix = app.config.get('APISPEC_URL_PREFIX', url_prefix)
        self.spec_url = app.config.get('APISPEC_SPEC_URL', spec_url)
        self.doc_url = app.config.get('APISPEC_DOC_URL', doc_url)
        self.document_options = document_options
        
        self.resource_converter = ResourceConverter(app,
                                                    self.spec,
                                                    self.document_options)
        self.view_converter = ViewConverter(app, self.spec, self.document_options)

        for deferred in self._deferred:
            deferred()

        self.add_doc_routes()

    def _defer(self, callable, *args, **kwargs):
        bound = functools.partial(callable, *args, **kwargs)
        self._deferred.append(bound)
        if self.app:
            bound()

    def add_doc_routes(self):
        bp_name = f"flask-apispec-{self.spec.version}"
        blueprint = flask.Blueprint(
            bp_name,
            __name__,
            template_folder='templates',
            url_prefix=self.url_prefix,
        )

        if self.spec_url:
            blueprint.add_url_rule(self.spec_url, 'spec', self.spec_json)

        if self.doc_url:
            @blueprint.route(self.doc_url)
            def doc():
                return flask.render_template("apidoc.html", spec_url=flask.url_for(f"{bp_name}.spec"), title=self.spec.title)

        self.app.register_blueprint(blueprint)

    def spec_json(self):
        return flask.jsonify(self.spec.to_dict()), 200, {
            "Access-Control-Allow-Origin": "*"
        }

    def register_existing_resources(self):
        for name, rule in self.app.view_functions.items():
            try:
                blueprint_name, _ = name.split('.')
            except ValueError:
                blueprint_name = None

            # Skip static rules
            if name == 'static':
                continue

            try:
                self.register(rule, blueprint=blueprint_name)
            except TypeError:
                pass

    def register(self, target, endpoint=None, blueprint=None,
                 resource_class_args=None, resource_class_kwargs=None):
        """Register a view.

        :param target: view function or view class.
        :param endpoint: (optional) endpoint name.
        :param blueprint: (optional) blueprint name.
        :param tuple resource_class_args: (optional) args to be forwarded to the
            view class constructor.
        :param dict resource_class_kwargs: (optional) kwargs to be forwarded to
            the view class constructor.
        """

        self._defer(self._register, target, endpoint, blueprint,
                    resource_class_args, resource_class_kwargs)

    def _register(self, target, endpoint=None, blueprint=None,
                  resource_class_args=None, resource_class_kwargs=None):
        """Register a view.

        :param target: view function or view class.
        :param endpoint: (optional) endpoint name.
        :param blueprint: (optional) blueprint name.
        :param tuple resource_class_args: (optional) args to be forwarded to the
            view class constructor.
        :param dict resource_class_kwargs: (optional) kwargs to be forwarded to
            the view class constructor.
        """
        from flask_apispec import ResourceMeta

        if isinstance(target, types.FunctionType):
            paths = self.view_converter.convert(target, endpoint, blueprint)
        elif isinstance(target, ResourceMeta):
            paths = self.resource_converter.convert(
                target,
                endpoint,
                blueprint,
                resource_class_args=resource_class_args,
                resource_class_kwargs=resource_class_kwargs,
            )
        else:
            raise TypeError()
        for path in paths:
            self.spec.path(**path)


def make_apispec(title='flask-apispec', version='v1', openapi_version='3.1.0'):
    return APISpec(
        title=title,
        version=version,
        openapi_version=openapi_version,
        plugins=[MarshmallowPlugin()],
    )
