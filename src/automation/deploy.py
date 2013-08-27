from fabric.api import *
from fabric.contrib import django
from fabric.contrib.console import confirm

from helpers import choose


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
        if env.python_interpreter:
            run("virtualenv env --python=%s" % env.python_interpreter)
        else:
            run("virtualenv env")
        run(
            "ln -sf %s %s/src/%s/settings/__init__.py" % (
                project_settings_path, new_instance_path, project_name))
        run("ln -sf %s %s/media" % (media_path, new_instance_path))
        with prefix('source %s/env/bin/activate' % new_instance_path):
            run("make deploy")

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
            run("python manage.py collectstatic --noinput")
            run("python manage.py compress")
            if env.deploy_role == 'production':
                if 'rax' in settings.INSTALLED_APPS:
                    run("python manage.py raxsync --all")
            if 'haystack' in settings.INSTALLED_APPS:
                run("python manage.py rebuild_index --noinput")


def deploy(branch, plan):
    if plan == 'fast':
        fast_deploy(branch)
    elif plan == 'full':
        full_deploy(branch)

    sudo("service apache2 restart", shell=False, pty=False)
    sudo("service memcached restart", shell=False, pty=False)
    sudo("service nginx restart", shell=False, pty=False)


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


def run_deploy(plan):
    if env.deploy_role == 'staging':
        execute(deploy, env.staging_branch, plan, role='staging')
    elif env.deploy_role == 'production':
        if plan == 'fast':
            if not confirm("Fast deploys to production are discouraged.  "
                           "Continue anyway?"):
                abort("Production fast deploy cancelled.")
        execute(deploy, env.production_branch, plan, role='production')


@task(default=True)
def interactive():
    server_options = ['staging', 'production']
    plan_options = ['fast', 'full']

    env.deploy_role = choose(
        "Where would you like to deploy?", server_options)
    plan = choose("What kind of deploy would you like to do?", plan_options)

    run_deploy(plan)
