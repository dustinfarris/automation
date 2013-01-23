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
  'repo_source',
  'project_name',
  'django_settings_module',
  'django_test_settings_module']
for required_setting in required_settings:
  if not hasattr(env, required_setting):
    raise RuntimeError('You must set %s in fabfile.py' % required_setting)

django.settings_module(env.django_settings_module)
