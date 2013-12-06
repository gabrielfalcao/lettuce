import json

from django.core.management import call_command

from leaves.models import *

from lettuce import after, step
from lettuce.django.steps.models import *

from nose.tools import assert_equals

after.each_scenario(clean_db)

max_rego = 0

@writes_models(Harvester)
def write_with_rego(step, update):
    data = hashes_data(step)
    for hash_ in data:
        hash_['rego'] = hash_['make'][:3].upper() + "001"
    write_models(Harvester, data, update)

@checks_existence(Harvester)
def check_with_rego(step):
    data = hashes_data(step)
    for hash_ in data:
        try:
            hash_['rego'] = hash_['rego'].upper()
        except KeyError:
            pass
    models_exist(Harvester, data)

@step(r'The database dump is as follows')
def database_dump(step):
    try:
        from cStringIO import StringIO
    except ImportError:
        from StringIO import StringIO
    output = StringIO()
    call_command('dumpdata', stdout=output, indent=2)
    output = output.getvalue()
    assert_equals(json.loads(output), json.loads(step.multiline))

@step(r'I have populated the database')
def database_populated(step):
    pass

@step(r'I count the harvesters')
def count_harvesters(step):
    print "Harvester count: %d" % Harvester.objects.count()
