# Django settings for cucumber project.

DEBUG = True
TEMPLATE_DEBUG = DEBUG

# Make this unique, and don't share it with anybody.
SECRET_KEY = '3c=9-_@gug3+!j*o*b$1!g8e7037(ghrns8pqygog1gs1f^zqu'

ROOT_URLCONF = 'cucumber.urls'

INSTALLED_APPS = (
    'lettuce.django',
    'first',
    'second',
)
