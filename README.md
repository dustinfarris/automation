Fabfile
=======

This module implements Fabric to perform the following tasks:

  * ``fab refresh`` to sync your database with the servers and rsync
    your media assets.
  * ``fab sync`` to pull changes from the master branch into your local
    topic branch.
  * ``fab merge`` to merge the changes from your topic branch back into
    master, or merge the master branch into the production branch.
  * ``fab deploy`` to run a "fast" or "full" deploy to either the
    staging or production servers.

To use this fabfile, git-clone it in your projects root directory, then
create fabfile/settings.py.  This file could be left empty, but you will
likely want to add your server settings.

Fabfile will automatically infer the project's name based on the root
project directory, and the Django settings module in the same way.

A simple settings.py file will probably just have these four lines:

    STAGING_SERVER_HOST = '123.123.123.11'
    STAGING_SERVER_USER = 'web'
    PRODUCTION_SERVER_HOST = '123.123.123.22'
    PRODUCTION_SERVER_USER = 'web'

Email any questions to
[dustin@dustinfarris.com](mailto:dustin@dustinfarris.com) or report
[issues on GitHub](https://github.com/dustinfarris/fabfile/issues)
