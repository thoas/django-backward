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

END_IGNORE_URLS = getattr(settings, 'BACKWARD_END_IGNORE_URLS', (
    '.xml',
    '.html',
))

URL_REDIRECT_NAME = getattr(settings, 'BACKWARD_URL_REDIRECT_NAME', 'url_redirect')

NEXT_ACTION_NAME = getattr(settings, 'BACKWARD_NEXT_ACTION_NAME', 'next_action')

DEFAULT_REDIRECT_URL = getattr(settings,
                               'BACKWARD_DEFAULT_REDIRECT_URL',
                               '/')
