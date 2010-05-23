.. _intro-overview:

========
Overview
========

On BDD
======

Behaviour-driven development is such a good approach to maintain a
plain workflow, wasting the time with what really matter: *business
value*.

The common TDD_ approach, consists basically in writing unit tests,
run, make it fail, write code, make it run, make it green. This is
such a awesome practice, since you can build really trustable code,
without wondering what can happen in the future of the project, thus
creating a huge amount of code that doesn't make sense.  Aditionally,
next steps use to be: do the same thing with functional, integration
and acceptance tests.

Nevertheless, BDD_ brings new perspectives to you, one of them is the
outside-in testing development. With this approach you can build your
software starting with the most external layer, and go deeper until
reach unitary tests.

Introducing Lettuce
===================

Lettuce is a quite simple tool, it is mostly based on Cucumber_, which
is a honking great tool, and has a lot more features than Lettuce.

Although Lettuce aims on the most usual tasks on BDD_, specially
focusing on those that make BDD_ be so fun :)

Lettuce pragma
==============

Give to developers ability to describe :ref:`features <intro-wtf>` in
natural language, composing it with one one or more scenarios.

Each scenario has one possible behaviour of the feature you want to implement.
To make the scenarios run python code, you define :ref:`steps <reference-steps`.

Hands on!
=========

This documentation will drive you through all the Lettuce features.
When you feel a bit comfortable, go to the :ref:`first part of the tutorial <tutorial-simple>`, or go further on the :ref:`reference <reference-features>`.

.. _Agile: http://agilemanifesto.org
.. _Cucumber: http://cukes.info
.. _TDD: http://en.wikipedia.org/wiki/Test_Driven_Development
.. _BDD: http://en.wikipedia.org/wiki/Behavior_Driven_Development
