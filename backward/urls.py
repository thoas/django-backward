from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^login/redirect/$',
        views.LoginRedirectView.as_view(),
        name='backward_login_redirect'),
]
