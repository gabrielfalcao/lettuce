.. _reference-features:

features, scenarios and steps reference
=======================================

Features, scenarios and steps are python objects within lettuce's
feature engine.

Here you will find out very "hacky" details about those objects. If
you stumbled here looking for a introduction, it might be a good idea
to read :ref:`the feature tutorial <tutorial-simple>` for a
introduction.


Feature
~~~~~~~

The class `Feature` is at lettuce's core, and after parsed and
resolved from a feature file, you can use those members:

In order to exemplify the usage of attributes and methods below, let's
consider that there is a feature in a file called `some.feature`

.. highlight:: ruby

::

    # language: en
    # just a comment

    # another one
    Feature: some feature
      Here comes
      The feature
      Description

      Scenario: ...
        ...

Feature.described_at
^^^^^^^^^^^^^^^^^^^^

a FeatureDescription object, has the file and line which the feature
was described. Lettuce uses it to output those metadata.


the attribute `described_at` could be used as follows

::

    # the line in which the feature started
    feature.described_at.line == 5

    # the filename path
    'some.feature' in feature.described_at.file

    # a tuple with the lines that contains the feature description
    feature.described_at.description_at == (6, 7, 8)

Feature.max_length
^^^^^^^^^^^^^^^^^^

A property that calculates the max length of all lines that built the
feature.

Mostly used by shell output to find out where to print the feature
description.

example:

::

    feature.max_length == 21

Feature.get_head
^^^^^^^^^^^^^^^^

does represent the feature with its first representation in current
language followed by a colon and the feature name.

example:

::

    feature.get_head() == 'Feature: some feature'

but if the same feature would written in brazillian portuguese, for example:

.. highlight:: ruby

::

        # language: pt-br
        # apenas um comentário

        # e outro
        Funcionalidade: alguma funcionalidade
          Aqui vem
          a descrição
          da funcionalidade

          Cenário: ...
            ...

then, `Feature.get_head()` would give:

::

    feature.get_head() == 'Funcionalidade: alguma funcionalidade'
