DEBUG = True

ROOT_URLCONF = 'alfaces_foo.urls'

INSTALLED_APPS = (
    'lettuce.django',
    'donothing', 
    'foobar',   
)

LETTUCE_APPS = (
    'foobar',
)
