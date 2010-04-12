.. _intro-install:

==================
Installing Lettuce
==================

Stable release
==============

You can install the latest stable release with pip

.. highlight:: bash

::

    user@machine:~$ [sudo] pip install lettuce


Using control version's HEAD
============================

You can use the bleeding edge version of Lettuce through taking the git HEAD.

If you want so, you have basically 2 options:

Build and install the egg from sources
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Good for those that just want to use the latest features

::

    user@machine:~/Downloads$ git clone git://github.com/gabrielfalcao/lettuce.git
    user@machine:~/Downloads$ cd lettuce
    user@machine:~/Downloads/lettuce$ sudo python setup.py install

Use the latest code to contribute with lettuce's codebase
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If it is your case, I strongly recommend a sandbox:

**GNU/Linux:**

#. Fetch the code

::

    user@machine:~/Projects$ git clone git://github.com/gabrielfalcao/lettuce.git

#. Add to your PYTHONPATH

::

    user@machine:~/Projects$ echo "PYTHONPATH=$HOME/Projects/lettuce:$PYTHONPATH >> $HOME/.bashrc

#. Open a new terminal and enjoy!
