DEBUG = True

ROOT_URLCONF = 'couves.urls'

INSTALLED_APPS = (
    'lettuce.django',
    'donothing', 
    'foobar',   
)

LETTUCE_APPS = (
    'foobar',
)
