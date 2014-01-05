from django.views import generic

from . import settings
from .helpers import get_url_redirect


class LoginRedirectView(generic.RedirectView):
    permanent = False

    def get_redirect_url(self, **kwargs):
        return get_url_redirect(self.request) or settings.DEFAULT_REDIRECT_URL
