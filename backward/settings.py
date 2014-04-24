from django.conf import settings

IGNORE_VIEWNAMES = getattr(settings, 'BACKWARD_IGNORE_VIEWNAMES', (
))

IGNORE_URLS = getattr(settings, 'BACKWARD_IGNORE_URLS', (
    settings.LOGIN_REDIRECT_URL,
    settings.LOGIN_URL,
))

if not hasattr(settings, 'BACKWARD_START_IGNORE_URLS'):
    START_IGNORE_URLS = (
        '/favicon',
        '/__debug__/',
    )

    if settings.MEDIA_URL and settings.MEDIA_URL.startswith('/'):
        START_IGNORE_URLS += (settings.MEDIA_URL, )

    if settings.STATIC_URL and settings.STATIC_URL.startswith('/'):
        START_IGNORE_URLS += (settings.STATIC_URL, )
else:
    START_IGNORE_URLS = settings.BACKWARD_START_IGNORE_URLS

END_IGNORE_URLS = getattr(settings, 'BACKWARD_END_IGNORE_URLS', (
    '.xml',
    '.html',
))

URL_REDIRECT_NAME = getattr(settings, 'BACKWARD_URL_REDIRECT_NAME', 'url_redirect')

NEXT_ACTION_NAME = getattr(settings, 'BACKWARD_NEXT_ACTION_NAME', 'next_action')

DEFAULT_REDIRECT_URL = getattr(settings,
                               'BACKWARD_DEFAULT_REDIRECT_URL',
                               '/')

LOGIN_URL = getattr(settings,
                    'BACKWARD_LOGIN_URL',
                    settings.LOGIN_URL)

IGNORE_AJAX = getattr(settings,
                      'BACKWARD_IGNORE_AJAX',
                      True)

LOGIN_REDIRECT_URL = getattr(settings,
                             'BACKWARD_LOGIN_REDIRECT_URL',
                             settings.LOGIN_REDIRECT_URL)


BACKEND_CLASS = getattr(settings,
                        'BACKWARD_BACKEND_CLASS',
                        'backward.backends.session.SessionBackend')

COOKIE_DOMAIN = getattr(settings, 'BACKWARD_COOKIE_DOMAIN', settings.SESSION_COOKIE_DOMAIN)

COOKIE_SECURE = getattr(settings, 'BACKWARD_COOKIE_SECURE', settings.SESSION_COOKIE_SECURE)

COOKIE_MAX_AGE = getattr(settings, 'BACKWARD_COOKIE_MAX_AGE', 3600)
