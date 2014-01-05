from django.conf.urls import patterns, url

from . import views


urlpatterns = patterns(
    '',
    url(r'^simple/$',
        views.simple,
        name='simple'),
)
