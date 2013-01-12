"""

A minimal Django app, just one file.

See: http://olifante.blogs.com/covil/2010/04/minimal-django.html

"""
import os
from django.conf.urls.defaults import patterns
from django.core.mail import send_mail

from django.http import HttpResponse
filepath, extension = os.path.splitext(__file__)
ROOT_URLCONF = os.path.basename(filepath)
INSTALLED_APPS = (
    "lettuce.django"
    )


def mail(request):
    send_mail('Subject here', 'Here is the message.', 'from@example.com',
             ['to@example.com'], fail_silently=False)
    return HttpResponse('Mail has been sent')

urlpatterns = patterns('', (r'^mail/$', mail))
