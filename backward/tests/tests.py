from django.test import TestCase


class BasicTests(TestCase):
    def test_simple(self):
        self.assertEqual(1, 1)
