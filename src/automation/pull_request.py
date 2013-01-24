from fabric.api import *
from fabric.contrib.console import confirm


@task(default=True)
def new():
  current_branch = local("git branch | grep '*'", capture=True)[2:]
  restricted_branches = [env.staging_branch, env.production_branch]
  for branch in restricted_branches:
    if branch == current_branch:
      abort("You cannot create pull requests from the %s branch." % branch)

  local("git push origin %s" % current_branch)
  if confirm(
    "Is this merge associated with a GitHub issue?",
    default=True):
    issue = prompt(
      "What is the issue number?",
      validate=int)
    local("hub pull-request -i %d -b %s" % (issue, env.production_branch))
  else:
    title = prompt("Title:")
    local("hub pull-request \"%s\" -b %s" % (title, env.production_branch))

  if confirm(
    "Pull-request complete.  Delete your branch '%s'?" % current_branch,
    default=False):
    local("git checkout %s" % env.production_branch)
    local("git branch -d %s" % current_branch)
