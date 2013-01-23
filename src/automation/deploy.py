from fabric.api import *
from fabric.contrib import django
from fabric.contrib.console import confirm


def full_deploy(branch):
  django.settings_module(env.django_settings_module)
  from django.conf import settings

  project_name = env.project_name
  project_path = '/var/www/%s' % project_name
  project_settings_path = '/var/www/.settings/%s.py' % project_name
  sites_path = '/var/www/.sites/'
  media_path = '/var/www/.media/%s' % project_name
  script_path = '/var/www/.scripts/%s.sh' % project_name
  system_now = run('date +\%Y\%m\%d\%H\%M\%S')
  new_instance_path = sites_path + project_name + "_" + system_now

  with cd(sites_path):
    existing_instances = run('ls|grep "%s_"' % project_name).split('\n')

  run("git clone %s %s" % (env.repo_source, new_instance_path))

  with cd(new_instance_path):
    run("git fetch origin")
    run("git checkout %s" % branch)
    run("git pull")
    run("git submodule init")
    run("git submodule update")
    run("virtualenv env")
    run(
      "ln -sf %s %s/%s/settings/__init__.py" % (
        project_settings_path, new_instance_path, project_name))
    with prefix('source %s/env/bin/activate' % new_instance_path):
      run("pip install --upgrade -r requirements.txt --use-mirrors")
      run("ln -s /usr/lib/python2.7/dist-packages/xapian/ "
          "env/lib/python2.7/site-packages/.")
      run("python manage.py migrate")
      run("python manage.py collectstatic --noinput")
      if 'haystack' in settings.INSTALLED_APPS:
        run("python manage.py rebuild_index --noinput")

  run("ln -sf %s %s/media" % (media_path, new_instance_path))
  run("ln -sfn %s %s" % (new_instance_path, project_path))

  run("source %s" % script_path)

  for old_instance in existing_instances:
    run("rm -rf %s%s" % (sites_path, old_instance))


def fast_deploy(branch):
  django.settings_module(env.django_settings_module)
  from django.conf import settings

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

      run("python manage.py migrate")
      if 'haystack' in settings.INSTALLED_APPS:
        run("python manage.py rebuild_index --noinput")
      run("python manage.py collectstatic --noinput")


def deploy(branch, plan):
  if plan == 'fast':
    fast_deploy(branch)
  elif plan == 'full':
    full_deploy(branch)

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
    execute(deploy, 'master', plan, role='staging')
  elif env.deploy_role == 'production':
    if plan == 'fast':
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
