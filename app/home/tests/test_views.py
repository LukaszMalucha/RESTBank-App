from django.test import TestCase, Client
from django.test.utils import override_settings
from django.urls import reverse

HOME_URL = reverse("home")

class HomeViewTests(TestCase):
    """Test main view"""

    def setUp(self):
        self.client = Client()

    def test_retrieving_home_view(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed("home.html")