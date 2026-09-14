import os

from django.conf import settings
from django.core.asgi import get_asgi_application

if settings.DEBUG:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "boilerplatejwt.settings.local")
else:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "boilerplatejwt.settings.production")

application = get_asgi_application()
