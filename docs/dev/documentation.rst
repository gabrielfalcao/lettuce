#################################
Contributing to the documentation
#################################

This documentation uses `Python-sphinx`_. It uses `reStructuredText`_ syntax.

***********
Conventions
***********

Language
========

The documentation is written in english.

Line length
===========

Limit all lines to a maximum of 79 characters.

Headings
========

Use the following symbols to create headings: ``#  *  =  -``

As an example:

.. highlight:: rst

::

  ##################
  H1: document title
  ##################

  *********
  Sample H2
  *********

  Sample H3
  =========

  Sample H4
  ---------

  And sample text.

If you need more than H4, then consider creating a new document.

Code blocks
===========

Combine a "highlight" directive and a "::" to specify the programming language.
As an example:

.. highlight:: rst

::

  .. highlight:: python

  ::

    import this

.. warning::

  "code-block" and "sourcecode" directives are not natively supported by
  rst2html, which is used by Github's repository browser, i.e. those lines
  won't appear on Github. Whereas "::" lines will.

Links and references
====================

On pages which are quite long, use links and references footnotes with the
"target-notes" directive. As an example:

.. highlight:: rst

::

  #############
  Some document
  #############

  Some text which includes links to `Example website`_ and many other links.

  `Example website`_ can be referenced multiple times.

  (... document content...)

  And at the end of the document...

  **********
  References
  **********

  .. target-notes::

  .. _`Example website`: http://www.example.com/

This :doc:`documentation` page uses this syntax.

**************
Install Sphinx
**************

`Python-sphinx`_ installation is covered in :doc:`/dev/install`.

In other cases, please refer to `Python-sphinx`_ documentation.

****************************
Export documentation to HTML
****************************

* Install `Python-sphinx`_.
* Make sure sphinx-build is in your shell's $PATH. If you are using virtualenv
  as told in :doc:`/dev/install`, then **activate your virtual environment**.
* Go to lettuce folder and use the provided Makefile:

  .. highlight:: sh

  ::

    make documentation

* HTML documentation is exported to docs/_build/html/.

*************
Use doctests!
*************

This documentation uses the `Sphinx's doctest extension`_.

Write doctests
==============

Here is a RST code sample to write doctests. You can find some doctests in
:doc:`/reference/terrain`.

.. highlight:: rst

::

  .. highlight:: python

  .. doctest::

     >>> print "Hello world!"
     Hello world!

See `Sphinx's doctest extension`_ and `Python's doctest`_ documentations for
details.

Run doctests
============

Go to lettuce folder and use the provided Makefile:

.. highlight:: sh

::

  make doctests

**********
References
**********

.. target-notes::

.. _`Python-sphinx`: http://sphinx.pocoo.org/
.. _`reStructuredText`: http://docutils.sourceforge.net/rst.html
.. _`Sphinx's doctest extension`: http://sphinx.pocoo.org/ext/doctest.html#module-sphinx.ext.doctest
.. _`Python's doctest`: http://docs.python.org/library/doctest.html
