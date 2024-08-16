"""
WSGI config for fndz_backend project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""
from django.core.wsgi import get_wsgi_application
from environment.base import set_environment
from environment.variables import EnvironmentVariable

set_environment('MAIN')
application = get_wsgi_application()
