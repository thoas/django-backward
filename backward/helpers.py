# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging

from django.http import HttpResponseRedirect, QueryDict
from django.core.urlresolvers import resolve

from .utils import scheme, load_class

from . import settings

logger = logging.getLogger('backward')

engine = load_class(settings.BACKEND_CLASS)()


def get_url_redirect(request):
    return engine.get_url_redirect(request)


def save_url_redirect(request, response, url_redirect):
    engine.save_url_redirect(request, response, url_redirect)


def save_next_action(request, response, data):
    engine.save_next_action(request, response, data)


def get_next_action(request):
    return engine.get_next_action(request)


def delete_next_action(request):
    engine.delete_next_action(request)


def run_next_action(request):
    data = None

    try:
        data = get_next_action(request)
    except Exception, e:
        logger.error(e)

    if not data or 'action' not in data:
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
        save_url_redirect(request, result['Location'])

        if 'redirect_url' in data:
            return HttpResponseRedirect(data['redirect_url'])

        return HttpResponseRedirect('%s://%s%s' % (scheme(request),
                                                   request.get_host(),
                                                   settings.LOGIN_REDIRECT_URL))
