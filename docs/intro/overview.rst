.. _intro-overview:

========
Overview
========

On BDD
======

Behaviour-driven development is a very good approach for maintaining
the workflow plain, so you only spend time with what really matters:
business value.

The common BDD approach basically consists in:

* writing some unit tests
* running these tests
* making these tests fail
* writing code
* making the code pass these tests (green status)

This is a very awesome practice, since you can build huge and reliable
software without fearing the future. You don't need to worry if those
millions of lines of code won't make sense in 10 years, as long as
they keep passing the tests. Despite BDD, other kind of tests are very
important and usually follow a similar workflow: functional,
integration and acceptance.

Nevertheless, BDD_ brings new perspectives to you, one of them is the
outside-in testing development. With this approach you can build your
software starting with the most external layer, and go deeper until
reach unitary tests.

Introducing Lettuce
===================

Lettuce is a very simple BDD tool based on the Cucumber, which
currently has many more features than Lettuce.

Lettuce aims the most common tasks on BDD and it focus specially on
those that make BDD so fun :)

Lettuce pragma
==============

Provide to the developers the ability of describing :ref:`features <intro-wtf>` in a natural language, by creating one or more scenarios

Each scenario has one possible behaviour of the feature you want to implement.
To make the scenarios run python code, it is necessary to define :ref:`steps <reference-features>`.

Hands on!
=========

This documentation will drive you through all the Lettuce features.
When you feel a bit comfortable, go to the :ref:`first part of the tutorial <tutorial-simple>`, or go further on the :ref:`reference <reference-features>`.
