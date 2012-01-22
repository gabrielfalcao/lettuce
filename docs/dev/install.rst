#############################################
Install a development environment for lettuce
#############################################

Here are guidelines to get a development environment for lettuce.

***********
OS specific
***********

Here are repcipes for specific operating systems. They should help you go fast
or automate lettuce installation procedure:

.. toctree::

   install-debian-squeeze

******************
Generic guidelines
******************

Dependencies
============

**you will need to install these dependencies in order to** *hack* **lettuce**
:)

All of them are used within lettuce tests.

you could use a virtualenv
--------------------------

.. highlight:: bash

::

  mkvirtualenv lettuce
  workon lettuce
  pip install -r requirements.txt

or just install manually
------------------------

.. highlight:: bash

::

  sudo pip install -r requirements.txt

or do it really from scratch
----------------------------

* [nose](http://code.google.com/p/python-nose/)
    > [sudo] pip install nose
* [mox](http://code.google.com/p/pymox/)
    > [sudo] pip install mox
* [sphinx](http://sphinx.pocoo.org/)
    > [sudo] pip install sphinx
* [lxml](http://codespeak.net/lxml/)
    > [sudo] pip install lxml
* [tornado](http://tornadoweb.org/)
    > [sudo] pip install tornado
* [django](http://djangoproject.com/)
    > [sudo] pip install django

Installing lettuce itself
=========================

.. highlight:: bash

::

  [sudo] python setup.py develop
