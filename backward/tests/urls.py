from django.conf.urls import patterns, url, include

from . import views


urlpatterns = patterns(
    '',

    url(r'^simple/$',
        views.simple,
        name='simple'),

    url(r'^login/simple/$',
        views.login_simple,
        name='login_simple'),

    url(r'^action/simple/$',
        views.action_simple,
        name='action_simple'),

    url(r'^auth/',
        include('django.contrib.auth.urls')),

    url(r'^backward/',
        include('backward.urls')),
)
