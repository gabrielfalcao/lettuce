.. _reference-languages:

language support
================

Lettuce currently supports two languages:

* English
* Portuguese (Brazilian)

Although it's only about writing tests since the current version
does output only in English.

writing features in a specific language
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can tell lettuce the language of a feature file through adding a comment in the first line of the file, using the following syntax:

.. highlight:: python

::

   # language: <code>

english example
^^^^^^^^^^^^^^^

.. highlight:: ruby

::

    # language: en
    Feature: write features in english
       Scenario: simple scenario
          Given I write a file which starts with "# language: en"
          Then it must be parsed with proper english keywords

brazilian portuguese example
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. highlight:: ruby

::

    # language: pt-br
    Funcionalidade: escrever funcionalidades em português
       Cenário: cenário simples
          Dado que eu crio um arquivo que começa com "# language: pt-br"
          Então ele deve ser interpretado com as devidas palavras-chave brasileiras

adding support to other languages
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

We love contribution, so if you want to bring lettuce to your native
language there is a single and simple way.

fetch the code
^^^^^^^^^^^^^^

First of all, you must have git_ control version installed in your machine.

Once you have it installed, grab the code with

.. highlight:: bash

::

   user@machine:~$ git clone git://github.com/gabrielfalcao/lettuce.git

And edit the file located at::

    lettuce/languages.py

And add a new dictionary entry for your native language.

Let's see the Brazilian Portuguese translation to exemplify.

.. highlight:: python

::

        LANGUAGES = {
            'pt-br': {
                'examples': u'Exemplos|Cenários',
                'feature': u'Funcionalidade',
                'name': u'Portuguese',
                'native': u'Português',
                'scenario': u'Cenário|Cenario',
                'scenario_outline': u'Esquema do Cenário|Esquema do Cenario',
                'scenario_separator': u'(Esquema do Cenário|Esquema do Cenario|Cenario|Cenário)',
            },
        }

The key of the dict will be used as identifier for the comment
``# language: identifier`` at feature files.

The value must be a dict, where the keys are canonical representation
of keywords (string), and the values must be a pipe-separated string
with translation possibilities.

It allows different translations for the same keyword in the current
language, which offers many possibilities for different semantical
cases.

For example, when using scenario outlines, it can be semantically nicer to write::

    Scenarios:
       | name | age |
       | John | 22  |
       | Mary | 53  |

Instead of::

    Examples:
       | name | age |
       | John | 22  |
       | Mary | 53  |

add your translation
^^^^^^^^^^^^^^^^^^^^

Now you can add your own language to lettuce, save the ``languages.py`` file and commit in the source control with.

For example, let's suppose that you've added Spanish support:

.. highlight:: bash

::

   user@machine:~/lettuce$ git commit lettuce/languages.py -m 'adding translation for spanish'

Generate a patch:

::

   user@machine:~/lettuce$ git format patch HEAD^1

And send to lettuce's ticket_ tracker as a gist_ or something like it.


.. _git: http://git-scm.com/
.. _ticket: http://github.com/gabrielfalcao/lettuce/issues
.. _gist: http://gist.github.com/
