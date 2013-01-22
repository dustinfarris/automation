from fabric.api import *


@task(default=True)
def sync():
  branch = local("git branch | grep '*'", capture=True)[2:]
  if branch == 'master':
    abort("You are already on the master branch!")
  local("git merge --no-ff --no-edit origin/master")
  local("git push origin %s" % branch)
