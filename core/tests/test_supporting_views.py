
import pprint
import json
from pprint import pprint

from django.test import TestCase

from core.models import Advertisement, DogBreed, Municipality, NewsEmail, Province
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

        # Create users
        cls.username1 = 'testuser1'
        cls.password1 = '1X<ISRUkw+tuK'

        cls.username2 = 'testuser2'
        cls.password2 = '2HJ1vRV0Z&3iD'

        cls.user1 = User.objects.create_user(username=cls.username1, password=cls.password1)

        cls.user2 = User.objects.create_user(username=cls.username2, password=cls.password2)
        cls.user2.news_email.is_active = True

        cls.user1.save()
        cls.user2.save()
        cls.user2.news_email.save()


    #setUp: Run once for every test method to setup clean data.
    def setUp(self):
        pass

    def test_unauthenticated_trying_to_change_subscription_status(self):
        response = self.client.post(f'/handle-email-subscription/{self.user1.news_email.uuid}')

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/accounts/login/')


    def test_authenticated_trying_to_change_subscription_status_from_deactivated_to_activated(self):
        self.client.login(username=self.username1, password=self.password1)
        response = self.client.post(f'/handle-email-subscription/{self.user1.news_email.uuid}')
        json_ = json.loads(response.content)

        self.assertEqual(json_, 'Activated')
        self.assertEqual(response.status_code, 200)


    def test_authenticated_trying_to_change_subscription_status_from_activated_to_deactivated(self):
        self.client.login(username=self.username2, password=self.password2)
        response = self.client.post(f'/handle-email-subscription/{self.user2.news_email.uuid}')
        json_ = json.loads(response.content)

        self.assertEqual(json_, 'Deactivated')
        self.assertEqual(response.status_code, 200)


    def test_provinces_returning_response(self):
        response = self.client.get('/ajax/load-provinces/')

        self.assertGreater(len(response.content), 1000)
        self.assertEqual(response.status_code, 200)

    def test_municipalities_returning_response(self):
        province_id = Province.objects.all().first().pk
        response = self.client.get('/ajax/load-municipalities/', {'province': province_id})

        self.assertGreater(len(response.content), 1000)
        self.assertEqual(response.status_code, 200)

    def test_areas_returning_response(self):
        municipality_id = Municipality.objects.filter(name="Stockholms stad").first().pk
        response = self.client.get('/ajax/load-areas/', {'municipality': municipality_id})

        self.assertGreater(len(response.content), 1000)
        self.assertEqual(response.status_code, 200)




    


