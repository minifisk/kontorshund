
import pprint
import json

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
        # Create two users
        cls.username1 = 'testuser1'
        cls.password1 = '1X<ISRUkw+tuK'

        cls.username2 = 'testuser2'
        cls.password2 = '2HJ1vRV0Z&3iD'

        cls.user1 = User.objects.create_user(username=cls.username1, password=cls.password1)
        cls.user2 = User.objects.create_user(username=cls.username2, password=cls.password2)

        cls.user1.save()
        cls.user2.save()


        cls.user_1_offering_ads = factories.create_offering_ads(count=5, user=cls.user1, is_published=True)
        cls.user_2_requesting_ads = factories.create_requesting_ads(count=10, user=cls.user2, is_published=True)


    #setUp: Run once for every test method to setup clean data.
    def setUp(self):
        pass


    def test_unauthenticated_trying_to_get_profile(self):
        response = self.client.get('/profile')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/accounts/login/?next=/profile')

    def test_authenticated_trying_to_access_profile(self):
        self.client.login(username=self.username1, password=self.password1)
        response = self.client.get('/profile')

        ad_title_1 = self.user_1_offering_ads[0].title

        json_response = json.dumps(response.content.decode("utf-8"))
        self.assertEqual(response.status_code, 200)
        self.assertIn(ad_title_1, json_response)
        self.assertNotIn('Mjau', json_response)

    
    def test_unauthenticated_trying_to_post_to_profile(self):
        response = self.client.get('/profile')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/accounts/login/?next=/profile')


    def test_authenticated_trying_to_post_to_profile_and_change_subscription(self):
        self.client.login(username=self.username1, password=self.password1)
        gbg_mun_obj= Municipality.objects.get(pk=179)

        NewsEmail_pre_change = vars(NewsEmail.objects.get(user__pk=self.user1.pk))
        
        body = {
            'province': ['15'], 
            'municipality': [gbg_mun_obj.pk], 
            'areas': ['12', '13', '16', '17', '14'], 
            'interval': ['2'], 
            'ad_type': ['1']
            }

        response = self.client.post('/profile', body)

        NewsEmail_post_change = NewsEmail.objects.get(user__pk=self.user1.pk).municipality.name


        self.assertEqual(NewsEmail_pre_change['province_id'], None)
        self.assertEqual(NewsEmail_post_change, gbg_mun_obj.name)
        self.assertEqual(response.status_code, 302)


    def test_getting_list_ads_initial_view(self):
        response = self.client.get('/postings/list')
        json_response = json.dumps(response.content.decode("utf-8"))

        self.assertEqual(response.status_code, 200)
        self.assertIn('(15)', json_response)
        self.assertIn('(5)', json_response)
        self.assertIn('(10)', json_response)

    def test_requesting_ads(self):
        pass




    


