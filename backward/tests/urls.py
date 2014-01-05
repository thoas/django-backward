from django.conf.urls import patterns, url, include

from . import views


urlpatterns = patterns(
    '',

    url(r'^simple/$',
        views.simple,
        name='simple'),

    url(r'^backward/', include('backward.urls')),
)
