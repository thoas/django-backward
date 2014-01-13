from django.test import TestCase
from django.contrib.auth.models import User
from django.test.utils import override_settings
from django.core.urlresolvers import reverse
from django.conf import settings as djsettings
from django.utils import importlib

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

    def test_ajax_simple(self):
        response = self.client.get(reverse('simple'), HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        self.assertEqual(response.status_code, 200)

        self.assertNotIn('url_redirect', self.client.session)

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

    def test_login_redirect(self):
        with override_settings(BACKWARD_START_IGNORE_URLS=(
            '/auth/',
        )):
            reload(settings)

            response = self.client.get(reverse('login_simple'))

            self.assertEqual(response.status_code, 302)

            self.assertEqual(self.client.session['url_redirect'], u'http://testserver/login/simple/')

            User.objects.create_user('newbie', 'newbie@example.com', '$ecret')

            response = self.client.post(reverse('login'), data={
                'username': 'newbie',
                'password': '$ecret'
            })

            self.assertRedirects(response,
                                 '/backward/login/redirect/',
                                 status_code=302,
                                 target_status_code=302)

            response = self.client.get(reverse('backward_login_redirect'))

            self.assertRedirects(response,
                                 'http://testserver/login/simple/',
                                 status_code=302,
                                 target_status_code=200)

    def test_action_simple(self):
        with override_settings(BACKWARD_START_IGNORE_URLS=(
            '/auth/',
        )):
            reload(settings)

            parameters = {
                'key': 'value'
            }

            response = self.client.post(reverse('action_simple'), data=parameters)

            self.assertEqual(response.status_code, 302)

            User.objects.create_user('newbie', 'newbie@example.com', '$ecret')

            response = self.client.post(reverse('login'), data={
                'username': 'newbie',
                'password': '$ecret'
            })

            response = self.client.get(reverse('backward_login_redirect'))

            for k, v in parameters.items():
                self.assertIn(k, self.client.session)
                self.assertEqual(self.client.session[k], v)
