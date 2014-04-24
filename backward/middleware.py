# -*- coding: utf-8 -*-
from django.core.urlresolvers import resolve, Resolver404

from .helpers import save_url_redirect, run_next_action
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

    def process_request(self, request):
        if request.user and request.user.is_authenticated():
            result = run_next_action(request)

            if result:
                return result

    def process_response(self, request, response):
        if not self._is_exempt(request):
            url_redirect = '%s://%s%s' % (scheme(request),
                                          request.get_host(),
                                          request.path_info)

            save_url_redirect(request, response, url_redirect)

        return response
