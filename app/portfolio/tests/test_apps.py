from django.test import TestCase

from portfolio.apps import PortfolioConfig


class PortfolioAppTests(TestCase):

    def test_app_name(self):

        self.assertEqual(PortfolioConfig.name, "portfolio")