"""
WSGI config for apiCrud project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os, sys
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.abspath(os.path.join(BASE_DIR, '..'))

sys.path.append(PROJECT_DIR)
os.environ['DJANGO_SETTINGS_MODULE'] = 'apiCrud.settings'

import django.core.handlers.wsgi
_application = django.core.handlers.wsgi.WSGIHandler()

def application(environ, start_response):
    os.environ['ESTIC_SERVER'] = environ['ESTIC_SERVER']
    return _application(environ, start_response)

