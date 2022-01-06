from django.test import TestCase, Client
from django.urls import reverse
client = Client()
class TestUrls(TestCase):
    def test_url1(self):
        response = self.client.get(reverse("availfood"))
        self.assertEqual(response.status_code, 200)

