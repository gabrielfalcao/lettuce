import django
from django.conf import settings
from django.contrib import admin
from django.conf.urls.defaults import *

admin.autodiscover()
django_version = django.get_version()

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
)

if django_version.startswith('1.3'):
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    urlpatterns += staticfiles_urlpatterns()

else:
    urlpatterns += (url(
        r'^static/(?P<path>.*)$',
        'django.views.static.serve',
        {
            'document_root': settings.STATIC_FILES_AT,
        },
    ),)
