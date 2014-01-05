import importlib

from django.test import TestCase
from django.test.utils import override_settings
from django.core.urlresolvers import reverse
from django.conf import settings as djsettings

from backward import settings


class BasicTests(TestCase):
    def setUp(self):
        settings.SESSION_ENGINE = 'django.contrib.sessions.backends.file'
        engine = importlib.import_module('django.contrib.sessions.backends.file')
        store = engine.SessionStore()
        store.save()

        self.session = store
        self.client.cookies[djsettings.SESSION_COOKIE_NAME] = store.session_key

        reload(settings)

    def test_simple(self):
        response = self.client.get(reverse('simple'))

        self.assertEqual(response.status_code, 200)

        self.assertEqual(self.client.session['url_redirect'], u'http://testserver/simple/')

    def test_ignorable(self):
        with override_settings(BACKWARD_IGNORE_VIEWNAMES=(
            'simple',
        )):
            reload(settings)

            response = self.client.get(reverse('simple'))

            self.assertEqual(response.status_code, 200)

            self.assertNotIn('url_redirect', self.client.session)

        with override_settings(BACKWARD_IGNORE_URLS=(
            '/simple/',
        )):
            reload(settings)

            response = self.client.get(reverse('simple'))

            self.assertEqual(response.status_code, 200)

            self.assertNotIn('url_redirect', self.client.session)
