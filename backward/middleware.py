# -*- coding: utf-8 -*-
from django.core.urlresolvers import resolve, Resolver404

from .helpers import get_url_redirect, set_url_redirect, run_next_action
from .utils import scheme
from . import settings


class BackwardMiddleware(object):
    def _is_exempt(self, request):
        exemptions = settings.IGNORE_URLS

        result = False

        path_info = request.META.get('PATH_INFO')

        if exemptions:
            try:
                match = resolve(path_info)
            except Resolver404:
                return False

            result = match and (match.url_name in exemptions)

        if result is False:
            result = path_info.startswith(settings.START_IGNORE_URLS) \
                or path_info.endswith(settings.END_IGNORE_URLS)

        return result

    def redirect_to_previous(self, request):
        update_url_redirect = True

        url_redirect = get_url_redirect(request)

        if self._is_exempt(request):
            update_url_redirect = False

        if update_url_redirect:
            url_redirect = '%s://%s%s' % (scheme(request),
                                          request.META.get('HTTP_HOST'),
                                          request.path_info)

        set_url_redirect(request, url_redirect)

    def process_request(self, request):
        if self._is_exempt(request):
            return

        result = self.redirect_to_previous(request)
        if result:
            return result

        if request.user and request.user.is_authenticated():
            result = run_next_action(request)

            if result:
                return result
