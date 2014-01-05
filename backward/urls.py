from django.conf.urls import patterns, url

from . import views


urlpatterns = patterns(
    '',
    url(r'^login/redirect/$',
        views.LoginRedirectView.as_view(),
        name='backward_login_redirect'),
)
