from fabric.api import *


@task(default=True)
def new():
  branch_name = prompt("New branch name:", validate=r'^[a-z0-9_-]{3,20}$')
  local("git checkout -b %s" % branch_name)
  local("git push -u origin %s" % branch_name)
