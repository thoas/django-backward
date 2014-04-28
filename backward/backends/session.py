try:
    import cPickle as pickle
except ImportError:
    import pickle

from .base import Backend

from backward import settings


class SessionBackend(Backend):
    def get_url_redirect(self, request):
        return request.session.get(settings.URL_REDIRECT_NAME, None)

    def save_url_redirect(self, request, response, url_redirect):
        request.session[settings.URL_REDIRECT_NAME] = url_redirect

    def get_next_action(self, request):
        if settings.NEXT_ACTION_NAME in request.session:
            return pickle.loads(request.session[settings.NEXT_ACTION_NAME])

        return {}

    def save_next_action(self, request, response, data):
        request.session[settings.NEXT_ACTION_NAME] = pickle.dumps(data, pickle.HIGHEST_PROTOCOL)

    def delete_next_action(self, request, response):
        try:
            del request.session[settings.NEXT_ACTION_NAME]
        except KeyError:
            return False

        return True
