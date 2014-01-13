# -*- coding: utf-8 -*-
from django.core.urlresolvers import resolve, Resolver404

from .helpers import get_url_redirect, set_url_redirect, run_next_action
from .utils import scheme
from . import settings


class BackwardMiddleware(object):
    def _is_exempt(self, request):
        if request.is_ajax() and settings.IGNORE_AJAX:
            return True

        exemptions = settings.IGNORE_VIEWNAMES

        result = False

        path_info = request.META.get('PATH_INFO')

        if exemptions:
            try:
                match = resolve(path_info)
            except Resolver404:
                pass
            else:
                result = match and (match.url_name in exemptions)

        if result is False:
            for url in settings.IGNORE_URLS:
                if url == path_info:
                    return True

            result = path_info.startswith(settings.START_IGNORE_URLS) \
                or path_info.endswith(settings.END_IGNORE_URLS)

        return result

    def manage_redirection(self, request):
        update_url_redirect = True

        url_redirect = get_url_redirect(request)

        if self._is_exempt(request):
            update_url_redirect = False

        if update_url_redirect:
            url_redirect = '%s://%s%s' % (scheme(request),
                                          request.get_host(),
                                          request.path_info)

        set_url_redirect(request, url_redirect)

    def process_request(self, request):
        if not self._is_exempt(request):
            result = self.manage_redirection(request)

            if result:
                return result

        if request.user and request.user.is_authenticated():
            result = run_next_action(request)

            if result:
                return result
