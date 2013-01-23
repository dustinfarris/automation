from fabric.api import *
from fabric.contrib.console import confirm


@task(default=True)
def new():
  current_branch = local("git branch | grep '*'", capture=True)[2:]
  restricted_branches = ['master', 'production']
  for branch in restricted_branches:
    if branch == current_branch:
      abort("You cannot create pull requests from the %s branch." % branch)

  local("git push origin %s" % current_branch)
  if confirm(
    "Is this merge associated with a GitHub issue?",
    default=False):
    issue = prompt(
      "What is the issue number?",
      validate=int)
    local("hub pull-request -i %d -b production" % issue)
  else:
    title = prompt("Title:")
    local("hub pull-request \"%s\" -b production" % title)
