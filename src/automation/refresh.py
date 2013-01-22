from fabric.api import *
from fabric.contrib.console import confirm
from django.conf import settings


def refresh():
  db_name = settings.DATABASES['default']['NAME']
  if not confirm("Are you sure you want to drop your %s database?" % db_name):
    abort("Refresh cancelled.")

  _system_date = "`date +\%Y\%m\%d`"
  sql_file_name = "%s.%s.sql.bz2" % (env.project_name, _system_date)

  dropdb = local("dropdb %s" % db_name)
  if dropdb.failed:
    print("Info: %s does not exist" % db_name)
  local("createdb %s" % db_name)
  base_path = "%s:/var/backups" % env.roledefs[env.refresh_role][0]
  local("scp %s/%s/sql/%s ." % (base_path, env.project_name, sql_file_name))
  local("bzcat %s | psql %s > /dev/null" % (sql_file_name, db_name))
  local("rm %s" % sql_file_name)
  local(
    "rsync -vauz --delete %s/%s/media/ media" % (base_path, env.project_name))
  if 'haystack' in settings.INSTALLED_APPS:
    local("python manage.py rebuild_index --noinput")


def _validate_refresh_role(refresh_role):
  refresh_role = refresh_role.strip().lower()
  if refresh_role not in env.roledefs.keys():
    raise ValueError("Choose one of %s." % ' or '.join(env.roledefs.keys()))
  return refresh_role


def get_refresh_role():
  if len(env.roledefs) > 1:
    prompt((
      "Which server would you like to refresh from "
      "(%s)?" % ' or '.join(env.roledefs.keys())),
      'refresh_role',
      default=env.roledefs.keys()[0],
      validate=_validate_refresh_role)
  else:
    env.refresh_role = env.roledefs.keys()[0]


@task(default=True)
def interactive():
  get_refresh_role()
  execute(refresh, role=env.refresh_role)
