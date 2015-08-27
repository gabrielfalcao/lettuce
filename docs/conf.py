# -*- coding: utf-8 -*-
# <Lettuce - Behaviour Driven Development for python>
# Copyright (C) <2010-2012>  Gabriel Falcão <gabriel@nacaolivre.org>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import sys

here = os.path.dirname(__file__)
parent = os.path.dirname(here)

sys.path.append(parent)
sys.path.append(os.path.join(here, '_ext'))

from lettuce import version, release

copyright = u'Gabriel Falcão <gabriel@nacaolivre.org>'

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.doctest',
    'sphinx.ext.todo',
    'sphinx.ext.coverage'
]

templates_path = ["_templates"]
source_suffix = '.rst'
master_doc = 'contents'
project = 'Lettuce'

rst_epilog = '''
.. _Lettuce: http://lettuce.it
.. _Python: http://python.org
.. _Ruby: http://ruby-lang.org/
.. _Agile: http://agilemanifesto.org
.. _Cucumber: http://cukes.info
.. _Pyccuracy: http://github.com/heynemann/pyccuracy
.. _TDD: http://en.wikipedia.org/wiki/Test_Driven_Development
.. _BDD: http://en.wikipedia.org/wiki/Behavior_Driven_Development
'''

release = "%s (%s release)" % (version, release)
today_fmt = '%B %d, %Y'

add_function_parentheses = True
add_module_names = True
show_authors = True
html_use_smartypants = True
html_copy_source = True
pygments_style = 'bw'
exclude_dirnames = ['.git']
html_style = 'lettuce-docs.css'
html_static_path = ["_static"]
html_last_updated_fmt = '%b %d, %Y'
html_translator_class = "adjusts.LettuceHTMLTranslator"
html_additional_pages = {}
