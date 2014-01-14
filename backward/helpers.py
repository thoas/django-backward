# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import pickle
import logging

from django.http import HttpResponseRedirect, QueryDict
from django.core.urlresolvers import resolve

from .utils import scheme

from . import settings

logger = logging.getLogger('backward')


def get_url_redirect(request):
    return request.session.get(settings.URL_REDIRECT_NAME, None)


def set_url_redirect(request, url_redirect):
    request.session[settings.URL_REDIRECT_NAME] = url_redirect


def save_next_action(request, data):
    request.session[settings.NEXT_ACTION_NAME] = pickle.dumps(data, pickle.HIGHEST_PROTOCOL)


def get_next_action(request):
    if settings.NEXT_ACTION_NAME in request.session:
        return pickle.loads(request.session[settings.NEXT_ACTION_NAME])

    return {}


def delete_next_action(request):
    try:
        del request.session[settings.NEXT_ACTION_NAME]
    except KeyError:
        pass


def run_next_action(request):
    data = None

    try:
        data = get_next_action(request)
    except Exception, e:
        logger.error(e)

    if not data or not 'action' in data:
        return False

    try:
        view, view_args, view_kwargs = resolve(data['action'])
    except Exception as e:
        logger.error(e)

        return False

    args = data.get('args', None) or []

    kwargs = data.get('kwargs', None) or {}
    kwargs['data'] = data

    if 'method' in data:
        request.method = data['method']

    parameters = data.get('parameters', None) or {}

    for key, values in parameters.items():
        setattr(request, key, QueryDict(values))

    try:
        result = view(request, *args, **kwargs)
    except Exception as e:
        logger.error(e)

        return False

    delete_next_action(request)

    if result and isinstance(result, HttpResponseRedirect):
        set_url_redirect(request, result['Location'])

        if 'redirect_url' in data:
            return HttpResponseRedirect(data['redirect_url'])

        return HttpResponseRedirect('%s://%s%s' % (scheme(request),
                                                   request.get_host(),
                                                   settings.LOGIN_REDIRECT_URL))
