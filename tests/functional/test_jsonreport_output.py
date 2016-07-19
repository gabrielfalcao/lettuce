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
#
# REMOVE THIS

from __future__ import unicode_literals
from contextlib import contextmanager
import json
import os
import lettuce

from mock import patch
from nose.tools import assert_equals, assert_true, with_setup
from lettuce import registry
from lettuce import Runner
from tests.functional.test_runner import feature_name, bg_feature_name
from tests.asserts import prepare_stdout


@contextmanager
def check_jsonreport(feature, filename=None):
    filename = filename or "lettucetests.json"
    with patch.object(json, "dump") as json_dump:
        yield

        os.remove(filename)
        assert_true(json_dump.called, "Function not called")
        content, file_handle = json_dump.mock_calls[0][1]

    assert_equals(content, OUTPUTS[feature])
    assert_equals(file_handle.name, filename)
    # check that we can dump it
    try:
        json.dumps(content)
    except (TypeError, ValueError):
        raise AssertionError('JSON report is not valid JSON:\n\n%s' % content)


@with_setup(prepare_stdout, registry.clear)
def test_jsonreport_output_with_no_errors():
    'Test jsonreport output with no errors'
    with check_jsonreport('commented_feature'):
        runner = Runner(feature_name('commented_feature'), enable_jsonreport=True)
        runner.run()


@with_setup(prepare_stdout, registry.clear)
def test_jsonreport_output_with_one_error():
    'Test jsonreport output with one errors'
    with check_jsonreport('error_traceback'):
        runner = Runner(feature_name('error_traceback'), enable_jsonreport=True)
        runner.run()


@with_setup(prepare_stdout, registry.clear)
def test_jsonreport_output_with_different_filename():
    'Test jsonreport output with different filename'
    with check_jsonreport('error_traceback', "custom_filename.json"):
        runner = Runner(
            feature_name('error_traceback'), enable_jsonreport=True,
            jsonreport_filename="custom_filename.json"
        )
        runner.run()


@with_setup(prepare_stdout, registry.clear)
def test_jsonreport_output_with_unicode_characters_in_error_messages():
    with check_jsonreport('unicode_traceback'):
        runner = Runner(feature_name('unicode_traceback'), enable_jsonreport=True)
        runner.run()

@with_setup(prepare_stdout, registry.clear)
def test_xunit_does_not_throw_exception_when_missing_step_definition():
    with check_jsonreport('missing_steps'):
        runner = Runner(feature_name('missing_steps'), enable_jsonreport=True)
        runner.run()


@with_setup(prepare_stdout, registry.clear)
def test_jsonreport_output_with_no_steps():
    'Test jsonreport output with no steps'
    with check_jsonreport('missing_steps'):
        runner = Runner(feature_name('missing_steps'), enable_jsonreport=True)
        runner.run()


@with_setup(prepare_stdout, registry.clear)
def test_jsonreport_output_with_background_section():
    'Test jsonreport output with a background section in the feature'
    @lettuce.step(ur'the variable "(\w+)" holds (\d+)')
    @lettuce.step(ur'the variable "(\w+)" is equal to (\d+)')
    def just_pass(step, *args):
        pass


    with check_jsonreport('background_simple'):
        runner = Runner(bg_feature_name('simple'), enable_jsonreport=True)
        runner.run()


@with_setup(prepare_stdout, registry.clear)
def test_jsonreport_output_with_unicode_and_bytestring():
    'Test jsonreport output with unicode and bytestring'
    with check_jsonreport('xunit_unicode_and_bytestring_mixing'):
        runner = Runner(feature_name('xunit_unicode_and_bytestring_mixing'), enable_jsonreport=True)
        runner.run()


BASE_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
OUTPUTS = {
    "commented_feature": {
        'features': [
            {'meta': {
                'steps': {
                    'failures': 0,
                    'skipped': 0,
                    'success': 1,
                    'total': 1,
                    'undefined': 0
                },
                'scenarios': {
                    'failures': 0,
                    'skipped': 0,
                    'success': 1,
                    'total': 1,
                    'undefined': 0
                }
            },
           'name': u'one commented scenario',
           'duration': 0,
           "background": None,
           'scenarios': [
                {'meta': {
                    'failures': 0,
                    'skipped': 0,
                    'success': 1,
                    'total': 1,
                    'undefined': 0
                },
                'name': u'Do nothing',
                'duration': 0,
                'outline': None,
                'steps': [
                    {'failure': {},
                    'meta': {
                        'failed': False,
                        'skipped': False,
                        'success': True,
                        'undefined': False
                    },
                    'duration': 0,
                    'name': u'Given I do nothing'
                }]
            }]
        }],
        'duration': 0,
        'meta': {
            'features': {
                'failures': 0,
                'success': 1,
                'total': 1
            },
            'is_success': True,
            'scenarios': {
                'failures': 0,
                'success': 1,
                'total': 1
            },
            'steps': {
                'failures': 0,
                'skipped': 0,
                'success': 1,
                'total': 1,
                'undefined': 0
            }
        }
    },
    'error_traceback': {
        "meta": {
            "scenarios": {
                "failures": 1,
                "total": 2,
                "success": 1
            },
            "is_success": False,
            "steps": {
                "failures": 1,
                "skipped": 0,
                "total": 2,
                "undefined": 0,
                "success": 1
            },
            "features": {
                "failures": 1,
                "total": 1,
                "success": 0
            }
        },
        "duration": 0,
        "features": [
            {
                "scenarios": [
                    {
                        "meta": {
                            "failures": 0,
                            "skipped": 0,
                            "total": 1,
                            "undefined": 0,
                            "success": 1
                        },
                        "steps": [
                            {
                                "failure": {},
                                "meta": {
                                    "failed": False,
                                    "skipped": False,
                                    "undefined": False,
                                    "success": True
                                },
                                'duration': 0,
                                "name": "Given my step that passes"
                            }
                        ],
                        "duration": 0,
                        "name": "It should pass",
                        "outline": None
                    },
                    {
                        "meta": {
                            "failures": 1,
                            "skipped": 0,
                            "total": 1,
                            "undefined": 0,
                            "success": 0
                        },
                        "steps": [
                            {
                                "failure": {
                                    "exception": "RuntimeError()",
                                    "traceback": "Traceback (most recent call last):\n  File \"{path}/lettuce/core.py\", line 144, in __call__\n    ret = self.function(self.step, *args, **kw)\n  File \"{path}/tests/functional/output_features/error_traceback/error_traceback_steps.py\", line 10, in given_my_step_that_blows_a_exception\n    raise RuntimeError\nRuntimeError\n".format(path=BASE_PATH)
                                },
                                "meta": {
                                    "failed": True,
                                    "skipped": False,
                                    "undefined": False,
                                    "success": False
                                },
                                'duration': 0,
                                "name": "Given my step that blows a exception"
                            }
                        ],
                        "duration": 0,
                        "name": "It should raise an exception different of AssertionError",
                        "outline": None
                    }
                ],
                'meta': {
                    'steps': {
                        "failures": 1,
                        "skipped": 0,
                        "total": 2,
                        "undefined": 0,
                        "success": 1
                    },
                    'scenarios': {
                        "failures": 1,
                        "skipped": 0,
                        "total": 2,
                        "undefined": 0,
                        "success": 1
                    }
                },
                "name": "Error traceback for output testing",
                "duration": 0,
                "background": None
            }
        ]
    },
    'unicode_traceback': {
        "meta": {
            "scenarios": {
                "failures": 1,
                "total": 2,
                "success": 1
            },
            "is_success": False,
            "steps": {
                "failures": 1,
                "skipped": 0,
                "total": 2,
                "undefined": 0,
                "success": 1
            },
            "features": {
                "failures": 1,
                "total": 1,
                "success": 0
            }
        },
        "duration": 0,
        "features": [
            {
                "scenarios": [
                    {
                        "meta": {
                            "failures": 0,
                            "skipped": 0,
                            "total": 1,
                            "undefined": 0,
                            "success": 1
                        },
                        "steps": [
                            {
                                "failure": {},
                                "meta": {
                                    "failed": False,
                                    "skipped": False,
                                    "undefined": False,
                                    "success": True
                                },
                                'duration': 0,
                                "name": "Given my dæmi that passes"
                            }
                        ],
                        "name": "It should pass",
                        "duration": 0,
                        "outline": None
                    },
                    {
                        "meta": {
                            "failures": 1,
                            "skipped": 0,
                            "total": 1,
                            "undefined": 0,
                            "success": 0
                        },
                        "steps": [
                            {
                                "failure": {
                                    "exception": "AssertionError()",
                                    "traceback": "Traceback (most recent call last):\n  File \"{path}/lettuce/core.py\", line 144, in __call__\n    ret = self.function(self.step, *args, **kw)\n  File \"{path}/tests/functional/output_features/unicode_traceback/unicode_traceback_steps.py\", line 10, in given_my_daemi_that_blows_a_exception\n    assert False\nAssertionError\n".format(path=BASE_PATH)
                                },
                                "meta": {
                                    "failed": True,
                                    "skipped": False,
                                    "undefined": False,
                                    "success": False
                                },
                                'duration': 0,
                                "name": "Given my \"dæmi\" that blows an exception"
                            }
                        ],
                        "name": "It should raise an exception different of AssertionError",
                        "duration": 0,
                        "outline": None
                    }
                ],
                "meta": {
                    "steps": {
                        "failures": 1,
                        "skipped": 0,
                        "total": 2,
                        "undefined": 0,
                        "success": 1
                    },
                    "scenarios": {
                        "failures": 1,
                        "skipped": 0,
                        "total": 2,
                        "undefined": 0,
                        "success": 1
                    }
                },
                "name": "Unicode characters in the error traceback",
                "duration": 0,
                "background": None
            }
        ]
    },
    "missing_steps": {
        "meta": {
            "scenarios": {
                "failures": 1,
                "total": 1,
                "success": 0
            },
            "is_success": True,
            "steps": {
                "failures": 0,
                "skipped": 0,
                "total": 1,
                "undefined": 1,
                "success": 0
            },
            "features": {
                "failures": 1,
                "total": 1,
                "success": 0
            }
        },
        "duration": 0,
        "features": [
            {
                "scenarios": [
                    {
                        "meta": {
                            "failures": 0,
                            "skipped": 0,
                            "total": 1,
                            "undefined": 1,
                            "success": 0
                        },
                        "steps": [
                            {
                                "failure": {},
                                "meta": {
                                    "failed": False,
                                    "skipped": False,
                                    "undefined": True,
                                    "success": False
                                },
                                'duration': None,  # undefined
                                "name": "Given my sdfsdf sdfsdf sdfs df sdfsdf"
                            }
                        ],
                        "name": "It should pass",
                        "duration": 0,
                        "outline": None
                    }
                ],
                "meta": {
                    "steps": {
                        "failures": 0,
                        "skipped": 0,
                        "total": 1,
                        "undefined": 1,
                        "success": 0
                    },
                    "scenarios": {
                        "failures": 0,
                        "skipped": 0,
                        "total": 1,
                        "undefined": 1,
                        "success": 0
                    }
                },
                "name": "Missing steps do not cause the xunit plugin to throw",
                "duration": 0,
                "background": None
            }
        ]
    },
    'no_steps_defined': {
        "meta": {
            "scenarios": {
                "failures": 1,
                "total": 1,
                "success": 0
            },
            "is_success": True,
            "steps": {
                "failures": 0,
                "skipped": 0,
                "total": 1,
                "undefined": 1,
                "success": 0
            },
            "features": {
                "failures": 1,
                "total": 1,
                "success": 0
            }
        },
        "duration": 0,
        "features": [
            {
                "scenarios": [
                    {
                        "meta": {
                            "failures": 0,
                            "skipped": 0,
                            "total": 1,
                            "undefined": 1,
                            "success": 0
                        },
                        "steps": [
                            {
                                "failure": {},
                                "meta": {
                                    "failed": False,
                                    "skipped": False,
                                    "undefined": True,
                                    "success": False
                                },
                                'duration': 0,
                                "name": "Given I do nothing"
                            }
                        ],
                        "name": "Do nothing",
                        "duration": 0,
                        "outline": None
                    }
                ],
                "meta": {
                    "steps": {
                        "failures": 0,
                        "skipped": 0,
                        "total": 1,
                        "undefined": 1,
                        "success": 0
                    },
                    "scenarios": {
                        "failures": 0,
                        "skipped": 0,
                        "total": 1,
                        "undefined": 1,
                        "success": 0
                    }
                },
                "name": "Scenario with no steps",
                "duration": 0,
                "background": None
            }
        ]
    },
    'xunit_unicode_and_bytestring_mixing': {
        "meta": {
            "scenarios": {
                "failures": 1,
                "total": 3,
                "success": 2
            },
            "is_success": False,
            "steps": {
                "failures": 1,
                "skipped": 0,
                "total": 3,
                "undefined": 0,
                "success": 2
            },
            "features": {
                "failures": 1,
                "total": 1,
                "success": 0
            }
        },
        "duration": 0,
        "features": [
            {
                "scenarios": [
                    {
                        "meta": {
                            "failures": 0,
                            "skipped": 0,
                            "total": 1,
                            "undefined": 0,
                            "success": 1
                        },
                        "steps": [
                            {
                                "failure": {},
                                "meta": {
                                    "failed": False,
                                    "skipped": False,
                                    "undefined": False,
                                    "success": True
                                },
                                'duration': 0,
                                "name": "Given non ascii characters \"Значение\" in outline"
                            }
                        ],
                        "name": "It should pass",
                        "duration": 0,
                        "outline": {
                            "value": "Значение"
                        }
                    },
                    {
                        "meta": {
                            "failures": 0,
                            "skipped": 0,
                            "total": 1,
                            "undefined": 0,
                            "success": 1
                        },
                        "steps": [
                            {
                                "failure": {},
                                "meta": {
                                    "failed": False,
                                    "skipped": False,
                                    "undefined": False,
                                    "success": True
                                },
                                'duration': 0,
                                "name": "Given non ascii characters \"\u0422\u0435\u0441\u0442\" in step"
                            }
                        ],
                        "name": "It should pass too",
                        "duration": 0,
                        "outline": None
                    },
                    {
                        "meta": {
                            "failures": 1,
                            "skipped": 0,
                            "total": 1,
                            "undefined": 0,
                            "success": 0
                        },
                        "steps": [
                            {
                                "failure": {
                                    "exception": "Exception(u'\\u0422\\u0435\\u0441\\u0442',)",
                                    "traceback": "Traceback (most recent call last):\n  File \"{path}/lettuce/core.py\", line 144, in __call__\n    ret = self.function(self.step, *args, **kw)\n  File \"{path}/tests/functional/output_features/xunit_unicode_and_bytestring_mixing/xunit_unicode_and_bytestring_mixing_steps.py\", line 16, in raise_nonascii_chars\n    raise Exception(word)\nException: \\u0422\\u0435\\u0441\\u0442\n".format(path=BASE_PATH)
                                },
                                "meta": {
                                    "failed": True,
                                    "skipped": False,
                                    "undefined": False,
                                    "success": False
                                },
                                'duration': 0,
                                "name": "Given non ascii characters \"\u0422\u0435\u0441\u0442\" in exception"
                            }
                        ],
                        "name": "Exception should not raise an UnicodeDecodeError",
                        "duration": 0,
                        "outline": None
                    }
                ],
                "meta": {
                    "steps": {
                        "failures": 1,
                        "skipped": 0,
                        "total": 3,
                        "undefined": 0,
                        "success": 2
                    },
                    "scenarios": {
                        "failures": 1,
                        "skipped": 0,
                        "total": 3,
                        "undefined": 0,
                        "success": 2
                    }
                },
                "name": "Mixing of Unicode & bytestrings in xunit xml output",
                "duration": 0,
                "background": None
            }
        ]
    },
    'background_simple': {
        "meta": {
            "scenarios": {
                "failures": 0,
                "total": 1,
                "success": 1
            },
            "is_success": True,
            "steps": {
                "failures": 0,
                "skipped": 0,
                "total": 1,
                "undefined": 0,
                "success": 1
            },
            "features": {
                "failures": 0,
                "total": 1,
                "success": 1
            }
        },
        "duration": 0,
        "features": [
            {
                "scenarios": [
                    {
                        "meta": {
                            "failures": 0,
                            "skipped": 0,
                            "total": 1,
                            "undefined": 0,
                            "success": 1
                        },
                        "steps": [
                            {
                                "failure": {},
                                "meta": {
                                    "failed": False,
                                    "skipped": False,
                                    "undefined": False,
                                    "success": True
                                },
                                'duration': 0,
                                "name": "Given the variable \"X\" is equal to 2"
                            }
                        ],
                        "name": "multiplication changing the value",
                        "duration": 0,
                        "outline": None
                    }
                ],
                "meta": {
                    "steps": {
                        "failures": 0,
                        "skipped": 0,
                        "total": 1,
                        "undefined": 0,
                        "success": 1
                    },
                    "scenarios": {
                        "failures": 0,
                        "skipped": 0,
                        "total": 1,
                        "undefined": 0,
                        "success": 1
                    }
                },
                "name": "Simple and successful",
                "duration": 0,
                "background": {
                    "meta": {
                        "total": 1,
                        "success": 1,
                        "failures": 0,
                        "skipped": 0,
                        "undefined": 0,
                    },
                    "steps": [
                        {
                            "failure": {},
                            "meta": {
                                "failed": False,
                                "skipped": False,
                                "undefined": False,
                                "success": True
                            },
                            'duration': 0,
                            "name": "Given the variable \"X\" holds 2"
                        }
                    ]
                }
            }
        ]
    }
}
