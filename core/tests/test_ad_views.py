
import pprint
import json

from django.test import TestCase

from core.models import Advertisement, DogBreed, Province
from core.tests import factories

from django.contrib.auth import get_user_model

User = get_user_model()

class TestAdViews(TestCase):
    fixtures = [
        '/home/dockeruser/web/core/fixtures/breeds.json', 
        '/home/dockeruser/web/core/fixtures/geographies.json', 
        '/home/dockeruser/web/core/fixtures/size_choices.json'
    ]

    #setUpTestData: Run once to set up non-modified data for all class methods.
    @classmethod
    def setUpTestData(cls):
        pass

    #setUp: Run once for every test method to setup clean data.
    def setUp(self):


        # Create two users
        self.username1 = 'testuser1'
        self.password1 = '1X<ISRUkw+tuK'

        self.username2 = 'testuser2'
        self.password2 = '2HJ1vRV0Z&3iD'

        self.user1 = User.objects.create_user(username=self.username1, password=self.password1)
        self.user2 = User.objects.create_user(username=self.username2, password=self.password2)

        self.user1.save()
        self.user2.save()


        self.user_1_ads = factories.create_offering_ads(count=5, user=self.user1, is_published=True)


    def test_unauthenticated_trying_to_access_profile(self):
        response = self.client.get('/profile')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/accounts/login/?next=/profile')

    def test_authenticated_trying_to_access_profile(self):
        self.client.login(username=self.username1, password=self.password1)
        response = self.client.get('/profile')

        ad_title_1 = self.user_1_ads[0].title

        json_response = json.dumps(response.content.decode("utf-8"))
        self.assertEqual(response.status_code, 200)
        self.assertIn(ad_title_1, json_response)
        self.assertNotIn('Mjau', json_response)

    


