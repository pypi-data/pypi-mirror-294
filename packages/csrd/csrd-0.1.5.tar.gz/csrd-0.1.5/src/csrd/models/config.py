from csrd_utils.config import _Config
from csrd_swaggerize.config import SwagConfig

class Config(_Config):
    _swagger: SwagConfig = None

    def __init__(self, *, swagger: SwagConfig = None):
        self._swagger = swagger

    def _init_swag(self):
        if self._swagger is None:
            self._swagger = SwagConfig()

    @property
    def swagger(self) -> SwagConfig:
        self._init_swag()
        return self._swagger

    @swagger.setter
    def swagger(self, swagger):
        self._swagger = swagger

    def compile(self):
        if self._swagger is not None:
            self._init_template()
            self._template['swagger'] = self._swagger.compile()
        return self._template
