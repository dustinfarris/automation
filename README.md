Automation
==========

[![Build Status](https://travis-ci.org/dustinfarris/automation.png?branch=master)](TravisCI)

This module implements Fabric to perform the following tasks:

  * ``fab refresh`` to sync your database with the servers and rsync
    your media assets.
  * ``fab topic`` to create a new topic-specific branch
  * ``fab sync`` to pull changes from the master branch into your local
    topic branch.
  * ``fab merge`` to merge the changes from your topic branch back into
    master, or merge the master branch into the production branch.
  * ``fab pull_request`` to submit a pull request on GitHub for your
    topic to be merged into the production branch
  * ``fab deploy`` to run a "fast" or "full" deploy to either staging or
    production servers

Installation
------------

Install via pip:

```sh
$ pip install automation
```

Create fabfile.py in your project's root directory and tell automation
about your project, then import automation:

```python
from fabric.api import env


env.project_name = 'myproject'
env.django_settings_module = 'myproject.settings'
env.django_test_settings_module = 'myproject.test_settings'
env.roledefs = {
  'staging': 'web@12.12.12.12',
  'production': 'web@45.45.45.45'}


from automation import *
```

Usage
-----

Exactly as mentioned above, just enter the command in your shell.  Note
that you must be in your project's directory (or a sub-directory)
thereof for Fabric to be able to find your fabfile.

e.g.

```sh
~/projects/myproject $ fab topic
```

Help
----

Email any questions to
[dustin@dustinfarris.com](mailto:dustin@dustinfarris.com) or report
[issues on GitHub](https://github.com/dustinfarris/automation/issues)
