from django.test import TestCase
from .models import contact
from django.urls import resolve
from django.urls import reverse



class contactTestCase(TestCase):
    @classmethod
    def setUp(cls):
        cls.obj = contact.objects.create(name="Rokibul Hasan",
                                         email="hasan@gmail.com",
                                         message="Not a good web app.")

    #def test_it_has_information_fields(self):
        #self.assertIsInstance(self.obj.name, str)
        #self.assertIsInstance(self.obj.email, str)
        #self.assertIsInstance(self.obj.message, str)

    def test_name_label(self):
        obj = contact.objects.get(id=1)
        field_label = obj._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'name')



#    def test_name_max_length(self):
#        obj = contact.objects.get(id=1)
#        max_length = obj._meta.get_field('name').max_length
#        self.assertEqual(max_length, 255)

class TestUrls(TestCase):
    def test_resolution_for_foo(self):
        response = self.client.get(reverse("contact_us"))
        self.assertEqual(response.status_code, 200)
