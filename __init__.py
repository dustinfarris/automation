from os.path import abspath, basename, dirname, join

from fabric.api import env
from fabric.contrib import django

import deploy
import merge
import refresh
import sync


repr(deploy)
repr(merge)
repr(refresh)
repr(sync)


env.project_name = basename(abspath(join(dirname(__file__), "../")))
env.django_settings_module = '%s.settings' % env.project_name
env.django_test_settings_module = '%s.settings.test' % env.project_name

django.settings_module(env.django_settings_module)
from django.conf import settings

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
