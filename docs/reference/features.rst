.. _reference-features:

features, scenarios and steps reference
=======================================

Features, scenarios and steps are python objects within lettuce's
feature engine.

Here you will find out very "hacky" details about those objects. If
you stumbled here looking for a introduction, it might be a good idea
to read :ref:`the feature tutorial <tutorial-simple>` for a
introduction.

In order to exemplify the usage of attributes and methods below, let's
consider that there is a feature in a file called ``some.feature``

.. highlight:: ruby

::

    # language: en
    # just a comment

    # another one
    Feature: some feature
      Here comes
      The feature
      Description

      Scenario: try out something
        Given I show lettuce running
        Then I should be happy

.. _feature-class:

Feature
~~~~~~~

Feature.name
^^^^^^^^^^^^

A string containing the name of the feature

.. highlight:: python

::

    feature.name == 'some feature'

Feature.scenarios
^^^^^^^^^^^^^^^^^

A list of scenario objects

The attribute ``scenarios`` could be used as follows

.. highlight:: python

::

    feature.scenarios[0].name == 'try out something'

Feature.described_at
^^^^^^^^^^^^^^^^^^^^

A FeatureDescription object, has the file and line which the feature
was described. Lettuce uses it to output those metadata.


The attribute ``described_at`` could be used as follows

::

    # the line in which the feature started
    feature.described_at.line == 5

    # the filename path
    'some.feature' in feature.described_at.file

    # a tuple with the lines that contains the feature description
    feature.described_at.description_at == (6, 7, 8)

Feature.max_length
^^^^^^^^^^^^^^^^^^

A property that calculates the maximum length of all lines that built
the feature.

Mostly used by shell output to find out where to print the feature
description.

Example:

::

    feature.max_length == 21

Feature.get_head
^^^^^^^^^^^^^^^^

Does represent the feature with its first representation in current
language followed by a colon and the feature name.

Example:

::

    feature.get_head() == 'Feature: some feature'

But if the same feature would written in Brazilian Portuguese, for example:

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

Then, ``Feature.get_head()`` would give:

::

    feature.get_head() == 'Funcionalidade: alguma funcionalidade'

.. _total-result:

TotalResult
~~~~~~~~~~~

TotalResult.features_ran
^^^^^^^^^^^^^^^^^^^^^^^^

Integer, the total of features ran

TotalResult.features_passed
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Integer, the total of features passed

TotalResult.scenarios_ran
^^^^^^^^^^^^^^^^^^^^^^^^^

Integer, the total of scenarios ran

TotalResult.scenarios_passed
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Integer, the total of scenarios passed

TotalResult.steps
^^^^^^^^^^^^^^^^^

Integer, the number of steps that were supposed to run

TotalResult.proposed_definitions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A list of :ref:`step-class` that have no :ref:`step-definition`

.. _scenario-class:

Scenario
~~~~~~~~

Scenario.steps
^^^^^^^^^^^^^^

A list of scenario objects

The attribute ``scenarios`` could be used as follows

.. highlight:: python

::

    scenario.steps[0].sentence == 'try out something'

.. _step-class:

Step
~~~~

Step.sentence
^^^^^^^^^^^^^

The string that represents the step

.. highlight:: python

::

    step.sentence == 'Given I show lettuce running'

.. _step-definition:

step definition
~~~~~~~~~~~~~~~

A decorator that can be used on any python function, takes a regex string as parameter, so that the function can me matched against steps.


.. highlight:: python

::

    from lettuce import step

    @step('I am (happy|sad)')
    def show_lettuce_running_here(step, action):
        if action == 'happy':
            return # everything is fine!

        else:
            assert False, 'you should be happy, dude!'
