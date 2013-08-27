from fabric.api import env
from fabric.contrib import django

import deploy
import pull_request
import refresh
import stage
import sync
import topic


repr(deploy)
repr(pull_request)
repr(refresh)
repr(stage)
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

env.production_branch = getattr(env, 'production_branch', 'master')
env.staging_branch = getattr(env, 'staging_branch', 'staging')
env.python_interpreter = getattr(env, 'python_interpreter', None)
django.settings_module(env.django_settings_module)
