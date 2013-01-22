from os.path import abspath, basename, dirname, join

from fabric.api import env
from fabric.contrib import django

import settings  # Create settings.py and override what you need to

import deploy
import merge
import refresh
import sync


repr(deploy)
repr(merge)
repr(refresh)
repr(sync)


PROJECT_NAME = getattr(
  settings, 'PROJECT_NAME', basename(abspath(join(dirname(__file__), "../"))))
DJANGO_SETTINGS_MODULE = getattr(
  settings, 'DJANGO_SETTINGS_MODULE', '%s.settings' % PROJECT_NAME)
DJANGO_TEST_SETTINGS_MODULE = getattr(
  settings, 'DJANGO_SETTINGS_MODULE', '%s.settings.test' % PROJECT_NAME)
STAGING_SERVER_USER = getattr(settings, 'STAGING_SERVER_USER', 'web')
STAGING_SERVER_HOST = getattr(settings, 'STAGING_SERVER_HOST', 'staging')
PRODUCTION_SERVER_USER = getattr(settings, 'PRODUCTION_SERVER_USER', None)
PRODUCTION_SERVER_HOST = getattr(settings, 'PRODUCTION_SERVER_HOST', None)

if STAGING_SERVER_HOST:
  staging_access = '%s%s' % (
    STAGING_SERVER_USER + '@' if STAGING_SERVER_USER else '',
    STAGING_SERVER_HOST)
  env.roledefs['staging'] = [staging_access]
if PRODUCTION_SERVER_HOST:
  production_access = '%s%s' % (
    PRODUCTION_SERVER_USER + '@' if PRODUCTION_SERVER_USER else '',
    PRODUCTION_SERVER_HOST)
  env.roledefs['production'] = [production_access]

env.project_name = PROJECT_NAME
django.settings_module(DJANGO_SETTINGS_MODULE)
