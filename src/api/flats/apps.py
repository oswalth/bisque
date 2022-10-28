from django.apps import AppConfig

from api import container


class FlatsConfig(AppConfig):
    name = 'api.flats'

    def ready(self):
        container.wire(modules=[".views"])
