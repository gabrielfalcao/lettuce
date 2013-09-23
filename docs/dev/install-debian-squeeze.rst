##############################
Installation on Debian Squeeze
##############################

Recipe to get a development environment for lettuce in a fresh install of
Debian Squeeze.

*********
Variables
*********

The following values are used below. You may customize them depending on your
needs.

.. highlight:: bash

::

  # Lettuce installation directory.
  lettuce_dir=~/lettuce
  # Virtualenv directory.
  lettuce_env_dir=$lettuce_dir
  # Git.
  upstream_url="https://github.com/gabrielfalcao/lettuce.git"
  fork_url=$upstream_url
  # System's package manager.
  system-install() { su -c "aptitude install ${*}" }

***************************
Install system dependencies
***************************

Execute the following commands:

.. highlight:: bash

::

  system-install python-dev python-virtualenv git libxml2-dev libxslt-dev

***********
Get sources
***********

.. highlight:: bash

::

  git clone $fork_url $lettuce_dir
  # Configure upstream
  cd $lettuce_dir
  git remote add upstream $upstream_url

*****************
Create virtualenv
*****************

.. highlight:: bash

::

  virtualenv --distribute --no-site-packages $lettuce_env_dir
  source $lettuce_env_dir/bin/activate
  cd $lettuce_dir
  pip install -r requirements.txt

*******************************
Install lettuce in develop mode
*******************************

.. highlight:: bash

::

  python setup.py develop

******************
Check installation
******************

You should be able to run lettuce and tests.

.. highlight:: bash

::

  lettuce --help

*****
Done!
*****

Go back to :doc:`/dev/index` and learn about :doc:`/dev/testing`.
