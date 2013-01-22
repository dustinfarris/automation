from fabric.api import *
from fabric.contrib.console import confirm


def merge_current_branch_into_master():
  branch = local("git branch | grep '*'", capture=True)[2:]
  if branch == 'master':
    abort("You are already on the master branch!")

  if not confirm(
    "This will merge all of your commits from %s "
    "into master.  Continue?" % branch):
    abort("Merge cancelled.")

  msg = "Merge branch '%s' into master" % branch

  local("git fetch --prune origin")
  local("git checkout master")
  local("git pull")
  local("git merge --no-ff --no-edit --commit -m \"%s\" %s" % (msg, branch))
  local("git push origin master")


@task(default=True)
def interactive():
  merge_current_branch_into_master()
  print "\nMerge complete.  You may now run `fab deploy`."
