from django.test import TestCase, Client
from .models import donateFood, donateMoney
from django.urls import reverse
client = Client()
class TestUrls(TestCase):
    def test_url1(self):
        response = self.client.get(reverse("donateMoney"))
        self.assertEqual(response.status_code, 200)


