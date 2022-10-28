import settings
from containers import Container

container = Container()
container.config.from_dict(settings.__dict__)
