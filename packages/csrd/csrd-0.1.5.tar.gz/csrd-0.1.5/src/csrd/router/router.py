from flask import Flask, redirect, url_for
from csrd.controller import Controller
from csrd.models import Config
from typing import Any

from csrd.utilities import Swaggerize


class Router:
    _flask_app: Flask = None
    _swaggerize: Swaggerize = None
    _config: Config = None
    _controllers = {}
    _models = {}
    _error_response = None

    def __init__(self, import_name: str, *, config: Config = None, error_response: Any = None):
        self._flask_app = Flask(import_name)
        self._config = config or Config()
        if error_response is not None:
            self._collect_model(error_response)
            self._error_response = error_response

    @property
    def app(self) -> Flask:
        return self._flask_app

    def _collect_model(self, model):
        if model is not None:
            name = model.__name__
            if name not in self._models:
                self._models[name] = model.schema()

    def register_controller(self, controller: 'Controller'):
        controller.default_models(error_response=self._error_response)
        controller.compile()
        self._controllers[controller.name] = controller
        self._config.swagger.add_definitions(controller.models)
        self.app.register_blueprint(getattr(controller, '_blueprint'))

    def run(self, host: str | None = None, port: int | None = None, debug: bool | None = None, load_dotenv: bool = True, **options: Any):
        self._config.swagger.add_definitions(self._models)
        self._swaggerize = Swaggerize(self.app, config=self._config.swagger)
        self.app.route('/')(lambda: redirect(url_for('flasgger.apidocs')))
        self.app.run(host, port, debug, load_dotenv, **options)
