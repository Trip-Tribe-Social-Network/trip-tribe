"""
WSGI config for trip_tribe project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os
import sys

# Add the project directory to the sys.path
path = '/home/JennyChen10/JennyChen10.pythonanywhere.com'
if path not in sys.path:
    sys.path.append(path)

# Set the default settings module for the 'django' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'trip_tribe.settings')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()