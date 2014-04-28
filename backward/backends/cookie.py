try:
    import cPickle as pickle
except ImportError:
    import pickle

from .base import Backend

from datetime import datetime, timedelta

from backward import settings


class CookieBackend(Backend):
    def get_url_redirect(self, request):
        return request.COOKIES.get(settings.URL_REDIRECT_NAME, None)

    def save_url_redirect(self, request, response, url_redirect):
        self.set_cookie(request, response, url_redirect, cookie_name=settings.URL_REDIRECT_NAME)

    def get_next_action(self, request):
        if settings.NEXT_ACTION_NAME in request.COOKIES:
            return pickle.loads(request.COOKIES[settings.NEXT_ACTION_NAME])

        return {}

    def save_next_action(self, request, response, data):
        self.set_cookie(request,
                        response,
                        pickle.dumps(data, pickle.HIGHEST_PROTOCOL),
                        cookie_name=settings.NEXT_ACTION_NAME)

    def delete_next_action(self, request, response):
        response.delete_cookie(settings.NEXT_ACTION_NAME, domain=self.get_cookie_domain(request))

    def set_cookie(self, request, response, value, cookie_name):
        max_age = settings.COOKIE_MAX_AGE

        expires = datetime.strftime(datetime.utcnow() + timedelta(seconds=max_age),
                                    "%a, %d-%b-%Y %H:%M:%S GMT")

        try:
            response.set_cookie(cookie_name,
                                value,
                                max_age=max_age,
                                expires=expires,
                                domain=self.get_cookie_domain(request),
                                secure=settings.COOKIE_SECURE or None)
        except UnicodeEncodeError:
            return False

        return True

    def get_cookie_domain(self, request):
        cookie_domain = settings.COOKIE_DOMAIN

        if cookie_domain and cookie_domain.startswith('.'):
            host = '.'.join(request.get_host().split('.')[-2:])

            cookie_domain = cookie_domain % {
                'host': host
            }

        return cookie_domain
