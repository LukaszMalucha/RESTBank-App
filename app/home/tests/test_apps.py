from django.test import TestCase

from home.apps import HomeConfig


class PortfolioAppTests(TestCase):

    def test_app_name(self):

        self.assertEqual(HomeConfig.name, "home")