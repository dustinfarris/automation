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

  if confirm(
    "Is this merge associated with a GitHub issue?",
    default=False):
    issue = prompt(
      "What is the issue number?",
      validate=int)
    msg += "; see issue #%d" % issue

  local("git fetch origin")
  local("git checkout master")
  local("git pull origin master")
  local("git merge --no-ff --no-edit --commit -m \"%s\" %s" % (msg, branch))
  local("git push origin master")


def merge_master_into_production():
  if not confirm(
    "Are you sure you want to merge the master branch into production?"):
    abort("Merge cancelled.")

  local("git fetch origin")
  local("git checkout production")
  local("git pull origin production")
  local("git merge --no-ff --edit --commit origin/master")
  local("git push origin production")


@task(default=True)
def interactive():
  plan = prompt((
    "What do you want to merge?\n\n"
    "* My current branch into [M]aster\n"
    "* The master branch into [P]roduction\n"
    "Enter (M or P):"),
    default='M',
    validate=r'(M|P|m|p)').lower()

  if plan == 'm':
    merge_current_branch_into_master()
  elif plan == 'p':
    merge_master_into_production()
  print "\nYou may now run `fab deploy`"
