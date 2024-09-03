from flask import Blueprint
from flask.sansio.scaffold import _sentinel, T_route, setupmethod
from flasgger import swag_from

from csrd.models import Config
from csrd.utilities.swaggerize import Swaggerize

from typing import Any, Callable, Dict, List
import os


class Controller:
    _blueprint: Blueprint = None
    _api_base_path: str
    _config: Config
    _models: dict = {}
    _routes: dict = {}

    _error_response = None

    def __init__(
            self,
            name: str,
            import_name: str,
            *,
            static_folder: str | os.PathLike[str] | None = None,
            static_url_path: str | None = None,
            template_folder: str | os.PathLike[str] | None = None,
            url_prefix: str | None = None,
            subdomain: str | None = None,
            url_defaults: dict[str, Any] | None = None,
            root_path: str | None = None,
            cli_group: str | None = _sentinel,  # type: ignore
    ):
        self._blueprint = Blueprint(name, import_name, static_folder=static_folder, static_url_path=static_url_path, template_folder=template_folder, url_prefix=url_prefix, subdomain=subdomain, url_defaults=url_defaults, root_path=root_path, cli_group=cli_group)

    @property
    def name(self):
        return self._blueprint.name

    @property
    def models(self):
        return self._models

    @property
    def routes(self):
        self._init_routes()
        return self._routes[self.name]

    def compile(self):
        routes = self.routes
        for rule in routes.keys():
            route: dict = routes[rule]

            f = route.pop('f')
            endpoint = route.pop('endpoint', None)
            request_model = route.pop('request_model', None)
            response_model = route.pop('response_model', None)
            error_response = route.pop('error_response',  None)
            if error_response is None:
                error_response = self._error_response

            self._blueprint.add_url_rule(rule, endpoint, f, **route)
            docs = self._build_docs(func=f, tags=[self.name], error_response=error_response, request_model=request_model, response_model=response_model)

            swag_from(specs=docs, endpoint=endpoint)(f)

    def _collect_model(self, model):
        if model is not None:
            name = model.__name__
            if name not in self._models:
                self._models[name] = model.schema()

    def default_models(self, error_response):
        self._error_response = error_response

    def _build_docs(self, func: T_route, tags: List[str], error_response=None, request_model=None, response_model=None) -> Dict[str, Any]:
        self._collect_model(request_model)
        self._collect_model(response_model)
        self._collect_model(error_response)

        kwargs = {
            "tags": tags,
            "request_model": request_model,
            "response_model": response_model,
            "error_response": error_response,
        }

        return Swaggerize.build_docs(func, **kwargs)

    @setupmethod
    def route(self, rule: str, *, error_response = None, **options: Any) -> Callable[[T_route], T_route]:
        """Decorate a view function to register it with the given URL
        rule and options. Calls :meth:`add_url_rule`, which has more
        details about the implementation.

        .. code-block:: python

            @app.route("/")
            def index():
                return "Hello, World!"

        See :ref:`url-route-registrations`.

        The endpoint name for the route defaults to the name of the view
        function if the ``endpoint`` parameter isn't passed.

        The ``methods`` parameter defaults to ``["GET"]``. ``HEAD`` and
        ``OPTIONS`` are added automatically.

        :param rule: The URL rule string.
        :param error_response: The object returned with a 500.
        :param options: Extra options passed to the
            :class:`~werkzeug.routing.Rule` object.
        """

        if error_response is None:
            error_response = self._error_response

        def decorator(f: T_route) -> T_route:
            endpoint = options.pop("endpoint", None)

            self._init_routes()

            self._routes[self.name][rule]['f'] = f
            self._routes[self.name][rule]['methods'] = options.pop("methods", ["GET"])
            self._routes[self.name][rule]['endpoint'] = endpoint
            self._routes[self.name][rule]['error_response'] = error_response
            return f

        return decorator

    def _method_route(
        self,
        method: str,
        rule: str,
        options: dict[str, Any], *, error_response=None
    ) -> Callable[[T_route], T_route]:
        if "methods" in options:
            raise TypeError("Use the 'route' decorator to use the 'methods' argument.")

        return self.route(rule, methods=[method], error_response=error_response, **options)

    def _init_routes(self):
        if self._routes is None:
            self._routes = {}

        if self.name not in self._routes.keys():
            self._routes[self.name] = {}


    @property
    def _check_setup_finished(self):
        return self._blueprint._check_setup_finished

    @setupmethod
    def get(self, rule: str, *, request_model=None, response_model=None, **options: Any) -> Callable[[T_route], T_route]:
        """Shortcut for :meth:`route` with ``methods=["GET"]``."""
        self._init_routes()
        self._routes[self.name][rule] = {'methods': ["GET"], "request_model": request_model, "response_model": response_model, **options}
        return self._method_route("GET", rule, options)

    @setupmethod
    def post(self, rule: str, *, request_model=None, response_model=None,  **options: Any) -> Callable[[T_route], T_route]:
        """Shortcut for :meth:`route` with ``methods=["POST"]``."""
        self._init_routes()
        self._routes[self.name][rule] = {'methods': ["POST"], "request_model": request_model, "response_model": response_model, **options}
        return self._method_route("POST", rule, options)

    @setupmethod
    def put(self, rule: str, *, request_model=None, response_model=None, **options: Any) -> Callable[[T_route], T_route]:
        """Shortcut for :meth:`route` with ``methods=["PUT"]``."""
        self._init_routes()
        self._routes[self.name][rule] = {'methods': ["PUT"], "request_model": request_model, "response_model": response_model, **options}
        return self._method_route("PUT", rule, options)

    @setupmethod
    def delete(self, rule: str, *, request_model=None, response_model=None, **options: Any) -> Callable[[T_route], T_route]:
        """Shortcut for :meth:`route` with ``methods=["DELETE"]``."""
        self._init_routes()
        self._routes[self.name][rule] = {'methods': ["DELETE"], "request_model": request_model, "response_model": response_model, **options}
        return self._method_route("DELETE", rule, options)

    @setupmethod
    def patch(self, rule: str, *, request_model=None, response_model = None, **options: Any) -> Callable[[T_route], T_route]:
        """Shortcut for :meth:`route` with ``methods=["PATCH"]``."""
        self._init_routes()
        self._routes[self.name][rule] = {'methods': ["PATCH"], "request_model": request_model, "response_model": response_model, **options}
        return self._method_route("PATCH", rule, options)
