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
    'backward',
    'backward.tests',
]

SECRET_KEY = 'blabla'

ROOT_URLCONF = 'backward.tests.urls'

try:
    from .temp import *  # noqa
except ImportError:
    pass


if django.VERSION <= (1, 6):
    TEST_RUNNER = 'discover_runner.DiscoverRunner'


MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'backward.middleware.BackwardMiddleware',
)

LOGIN_REDIRECT_URL = '/backward/login/redirect/'

SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer'
