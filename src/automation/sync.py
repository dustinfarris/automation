from fabric.api import *


@task(default=True)
def sync():
  current_branch = local("git branch | grep '*'", capture=True)[2:]
  if current_branch == env.staging_branch:
    abort("You are on the %s branch!" % env.staging_branch)
  local("git merge --no-ff --no-edit origin/%s" % env.staging_branch)
  local("git push origin %s" % current_branch)
