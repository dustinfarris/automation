from os.path import abspath, basename, dirname, join

from fabric.api import env
from fabric.contrib import django

import deploy
import merge
import pull_request
import refresh
import sync
import topic

repr(deploy)
repr(merge)
repr(pull_request)
repr(refresh)
repr(sync)
repr(topic)


required_settings = [
  'project_name', 'django_settings_module', 'django_test_settings_module']
for required_setting in required_settings:
  if not hasattr(env, required_setting):
    raise RuntimeError('You must set %s in fabfile.py' % required_setting)

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
