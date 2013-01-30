from fabric.api import *
from fabric.contrib.console import confirm


def merge_current_branch_into_staging_branch():
    current_branch = local("git branch | grep '*'", capture=True)[2:]
    if current_branch == env.staging_branch:
        abort("You are already on the %s branch!" % env.staging_branch)

    if not confirm("This will merge all of your commits from %s into %s.  "
                   "Continue?" % (current_branch, env.staging_branch)):
        abort("Merge cancelled.")

    msg = "Merge branch '%s' into %s" % (current_branch, env.staging_branch)

    local("git fetch --prune origin")
    local("git checkout %s" % env.staging_branch)
    local("git pull")
    local("git merge --no-ff --no-edit --commit "
          "-m \"%s\" %s" % (msg, current_branch))
    local("git push origin %s" % env.staging_branch)
    local("git checkout %s" % current_branch)


@task(default=True)
def interactive():
    merge_current_branch_into_staging_branch()
    print "\nMerge complete.  You may now run `fab deploy`."
