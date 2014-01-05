from django.test import TestCase
from django.core.urlresolvers import reverse


class BasicTests(TestCase):
    def test_simple(self):

        response = self.client.get(reverse('simple'))

        self.assertEqual(response.status_code, 200)
