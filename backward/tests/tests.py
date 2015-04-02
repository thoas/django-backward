import mock

from django.test import TestCase
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.conf import settings as djsettings
from django.utils.encoding import smart_text

try:
    from importlib import import_module
except ImportError:
    from django.utils.importlib import import_module

from backward import settings
from backward.helpers import engine


class BasicTests(TestCase):
    def setUp(self):
        settings.SESSION_ENGINE = 'django.contrib.sessions.backends.file'
        engine = import_module('django.contrib.sessions.backends.file')
        store = engine.SessionStore()
        store.save()

        self.session = store
        self.client.cookies[djsettings.SESSION_COOKIE_NAME] = store.session_key

    def test_ajax_simple(self):
        response = self.client.get(reverse('simple'), HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        self.assertEqual(response.status_code, 200)

        self.assertNotIn('url_redirect', self.client.session)

    def test_simple(self):
        response = self.client.get(reverse('simple'))

        self.assertEqual(response.status_code, 200)

        self.assertEqual(self.client.session['url_redirect'], u'http://testserver/simple/')

    def test_ignorable(self):
        with mock.patch.object(settings, 'IGNORE_VIEWNAMES', (
            'simple',
        )):
            response = self.client.get(reverse('simple'))

            self.assertEqual(response.status_code, 200)

            self.assertNotIn('url_redirect', self.client.session)

        with mock.patch.object(settings, 'IGNORE_URLS', (
            '/simple/',
        )):
            response = self.client.get(reverse('simple'))

            self.assertEqual(response.status_code, 200)

            self.assertNotIn('url_redirect', self.client.session)

    def test_login_redirect(self):
        with mock.patch.object(settings, 'START_IGNORE_URLS', (
            '/auth/',
        )):
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
        with mock.patch.object(settings, 'START_IGNORE_URLS', (
            '/auth/',
        )):
            parameters = {
                smart_text('key'): 'value'
            }

            response = self.client.post(reverse('action_simple'), data=parameters)

            self.assertEqual(response.status_code, 302)

            User.objects.create_user('newbie', 'newbie@example.com', '$ecret')

            data = engine.get_next_action(self.client)

            assert 'parameters' in data
            assert 'POST' in data['parameters']

            response = self.client.post(reverse('login'), data={
                'username': 'newbie',
                'password': '$ecret'
            })

            response = self.client.get(reverse('backward_login_redirect'))

            assert 'sent' in self.client.session
            assert self.client.session['sent'] is True
