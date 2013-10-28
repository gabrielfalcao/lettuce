from django.conf.urls import patterns, include, url

from .views import WaitView
urlpatterns = patterns('',
    url(r'^$', WaitView.as_view(), name='home'),
)
