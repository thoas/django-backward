import django

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

SITE_ID = 1
DEBUG = True

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'social.apps.django_app.default',
    'backward',
    'backward.tests',
]

SECRET_KEY = 'blabla'

ROOT_URLCONF = 'backward.urls'

try:
    from .temp import *  # noqa
except ImportError:
    pass


if django.VERSION <= (1, 6):
    TEST_RUNNER = 'discover_runner.DiscoverRunner'
