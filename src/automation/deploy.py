from fabric.api import *
from fabric.contrib import django


def deploy(branch, plan):
  with prefix('source /var/www/%s/env/bin/activate' % env.project_name):
    with cd('/var/www/%s' % env.project_name):
      server_branch = run("git branch")
      if "* %s" % branch not in server_branch:
        abort("The server is not on the %s branch" % branch)
      server_status = run("git status")
      if "Changes to be comitted" in server_status:
        abort("There are uncomitted changes on the server.")
      run("git pull")
      run("git submodule init")
      run("git submodule update")
      if plan == 'full':
        run("pip install --upgrade -r requirements.txt --use-mirrors")
      run("python manage.py migrate")
      run("python manage.py rebuild_index --noinput")
      run("python manage.py collectstatic --noinput")
  sudo("service apache2 restart", shell=False)
  sudo("service memcached restart", shell=False)
  sudo("service nginx restart", shell=False)


def test_branch(branch):
  status = local("git status")
  if "Changes" in status:
    abort("You have changes in your current branch.  "
          "Please stash these first before running a full deploy.")
  local("git checkout %s" % branch)
  local("git pull origin %s" % branch)
  local("git submodule init")
  local("git submodule update")
  local("make develop")
  django.settings_module(env.django_test_settings_module)
  if not local("make test").succeeded:
    abort("Testing failed for the %s branch." % branch)
  django.settings_module(env.django_settings_module)


def get_deploy_role():
  prompt(
    "Where would you like to deploy (staging or production)?",
    'deploy_role',
    default='staging',
    validate=r'(staging|production)')


def run_deploy(plan):
  if env.deploy_role == 'staging':
    if plan == 'full':
      test_branch('master')
    execute(deploy, 'master', plan, role='staging')
  elif env.deploy_role == 'production':
    if plan == 'full':
      test_branch('production')
    elif plan == 'fast':
      if not confirm(
        "Fast deploys to production are discouraged.  Continue anyway?"):
        abort("Production fast deploy cancelled.")
    execute(deploy, 'production', plan, role='production')


@task(default=True)
def interactive():
  get_deploy_role()
  plan = prompt(
    "What kind of deploy would you like to do (fast or full)?",
    default='full' if env.deploy_role == 'production' else 'fast',
    validate=r'(fast|full)')
  run_deploy(plan)
