from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User

from part1.models import CustomUser, PickUppoints, Volunteer

MODELS = [CustomUser]

class SampleModelViewTests(TestCase):
    fixtures = ['test_data',]

    def setUp(self):
        self.client = Client()
        self.test_user = User.objects.create_user('testuser', 'blah@blah.com', 'testpassword69!')
        self.test_user.is_superuser = True
        self.test_user.is_active = True
        self.test_user.save()
        self.assertEqual(self.test_user.is_superuser, True)
        login = self.client.login(username='testuser', password='testpassword69!')
        self.failUnless(login, 'Could not log in')

    #def tearDown(self):
        #for model in MODELS:
            #for obj in model.objects.all():
                #obj.delete()

    #def test_samplemodel_list(self):

        #test_response = self.client.get('/home/')
        #self.assertEqual(test_response.status_code, 200)
        #self.assertTrue('samplemodel_list' in test_response.context)
        #self.assertTemplateUsed(test_response, 'home.html')
        #self.assertEqual(test_response.context['home'][1].pk, 1)
        #self.assertEqual(test_response.context['home'][1].name, u'Sample Model Instance Name')

    def test_home_view(self):
        test_response = self.client.get('')
        self.assertEqual(test_response.status_code, 200)
        self.assertTrue('home' in test_response.context)
        self.assertTemplateUsed(test_response, 'home.html')
        self.assertEqual(test_response.context['home'].pk, 1)
        self.assertEqual(test_response.context['home'].name, u'Sample Model Instance Name')
