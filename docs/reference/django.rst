.. _reference-django:

=====================
Built-in Django Steps
=====================

Lettuce features a number of built-in steps for Django to simplify the
creation of fixtures.

*********************
creating fixture data
*********************

Lettuce can automatically introspect your available Django models to create
fixture data, e.g.

.. highlight:: ruby

::

    Background:
        Given I have options in the database:
            | name    | value |
            | Lettuce | Rocks |

This will find a model whose verbose name is *options*. It will then create
objects for that model with the parameters specified in the table (i.e.
``name=Lettuce``, ``value=Rocks``).

You can also specify relational information. Assuming a model ``Profile`` with
foreign key *user* and field *avatar*:

.. highlight:: ruby

::

    Background:
        Given user with username "harvey" has profile in the database:
            | avatar  |
            | cat.jpg |

To create many-to-many relationships, assuming ``User`` has and belongs to
many ``Group`` objects:

.. highlight:: ruby

::

    Background:
        Given user with username "harvey" is linked to groups in the database:
            | name |
            | Cats |

For many-to-many relationship to be created, both models must exist prior to
linking.

Most common data can be parsed, i.e. true/false, digits, strings and dates in
the form ``2013-10-30``.

registering your own model creators
-----------------------------------

For more complex models that have to process or parse data you can write your
own creating steps using the ``creates_models`` decorator.

.. highlight:: python

::

    from lettuce.django.steps.models import (creates_models,
                                             reset_sequence,
                                             hashes_data)

    @creates_models(Note)
    def create_note(step):
        data = hashes_data(step)
        for row in data:
            # convert the author into a user object
            row['author'] = get_user(row['author'])
            Note.objects.create(**row)

        reset_sequence(Note)

**************
testing models
**************

Two steps exist to test models.

.. highlight:: ruby

::

    Then features should be present in the database:
        | name    | value |
        | Lettuce | Rocks |
    And there should be 1 feature in the database

You can also test non-database model attributes by prefixing an ``@`` to the
attribute name. Non-database attributes are tested after the records are
selected from the database.

.. highlight:: ruby

::

    Then features should be present in the database:
        | name    | value | @language |
        | Lettuce | Rocks | Python    |

registering your own model testers
-----------------------------------

For more complex tests that have to process or parse data you can write your
own creating steps using the ``checks_existence`` decorator.

*********************
settings.py variables
*********************

``LETTUCE_APPS`` -- apps to test by default

``LETTUCE_USE_TEST_DATABASE`` -- use a test database instead of the live
database. Equivalent of ``-T`` flag.

other considered variables
--------------------------

``SOUTH_TESTS_MIGRATE`` -- apply a south migration to the test database
