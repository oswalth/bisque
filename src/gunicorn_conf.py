import multiprocessing

import environs


env = environs.Env()

DJANGO_HOST = env.str("DJANGO_HOST", "0.0.0.0")
DJANGO_PORT = env.int("DJANGO_PORT", 9050)


# Main config
# https://docs.gunicorn.org/en/latest/settings.html#config-file
wsgi_app = "api.wsgi:application"

# Logging
# https://docs.gunicorn.org/en/latest/settings.html#logging
accesslog = env.str("GUNICORN_ACCESS_LOG", "-")
errorlog = env.str("GUNICORN_ERROR_LOG", "-")
loglevel = env.str("GUNICORN_LOG_LEVEL", "info")

# Server socket
# https://docs.gunicorn.org/en/latest/settings.html#server-socket
bind = [f"{DJANGO_HOST}:{DJANGO_PORT}"]

# Worker Processes
# https://docs.gunicorn.org/en/latest/settings.html#worker-processes
workers = env.int("GUNICORN_WORKERS", multiprocessing.cpu_count() * 2)
timeout = env.int("GUNICORN_TIMEOUT", 30)
graceful_timeout = env.int("GUNICORN_GRACEFUL_TIMEOUT", 30)
