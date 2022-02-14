
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

        cls.user1.save()
        cls.user2.save()

        # Create ads

        # subtotal 1
        cls.count_offering_stockholm_stockholms_stad = 5
        cls.count_offering_stockholm_stockholms_stad_katarina_sofia = 1
        cls.count_offering_halland_falkenberg = 1
        cls.count_offering_halland_halmstad = 1

        cls.total_offering_count = (
            cls.count_offering_halland_falkenberg + 
            cls.count_offering_halland_falkenberg + 
            cls.count_offering_stockholm_stockholms_stad + 
            cls.count_offering_stockholm_stockholms_stad_katarina_sofia 
        )

        # subtotal 2
        cls.count_requesting_stockholm_stockholms_stad = 10
        cls.total_requesting_count = cls.count_requesting_stockholm_stockholms_stad

        # total
        cls.total_count = cls.total_offering_count + cls.total_requesting_count

        # creation
        cls.user_1_offering_ads_stockholm_stockholms_stad = factories.create_offering_ads_stockholm_stockholms_stad(count=cls.count_offering_stockholm_stockholms_stad, user=cls.user1, is_published=True)
        cls.user_2_requesting_ads_sthlm = factories.create_requesting_ads_stockholm_stockholms_stad(count=cls.count_requesting_stockholm_stockholms_stad, user=cls.user2, is_published=True)
       
        cls.user_2_offering_ads_halland_falkenberg = factories.create_offering_ads_halland_falkenberg(count=cls.count_offering_halland_falkenberg, user=cls.user2, is_published=True)
        cls.user_2_offering_ads_halland_halmstad = factories.create_offering_ads_halland_halmstad(count=cls.count_offering_halland_halmstad, user=cls.user2, is_published=True)
        
        cls.user_2_offering_ads_stockholm_stockholms_stad_katarina_sofia = factories.create_offering_ads_stockholm_stockholm_stad_katarina_sofia(count=cls.count_offering_stockholm_stockholms_stad_katarina_sofia, user=cls.user2, is_published=True)




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

        ad_title_1 = self.user_1_offering_ads_stockholm_stockholms_stad[0].title

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
        halland_mun_obj= Municipality.objects.get(pk=179)

        NewsEmail_pre_change = vars(NewsEmail.objects.get(user__pk=self.user1.pk))
        
        data = {
            'province': ['15'], 
            'municipality': [halland_mun_obj.pk], 
            'areas': ['12', '13', '16', '17', '14'], 
            'interval': ['2'], 
            'ad_type': ['1']
            }

        response = self.client.post('/profile', data)

        NewsEmail_post_change = NewsEmail.objects.get(user__pk=self.user1.pk).municipality.name


        self.assertEqual(NewsEmail_pre_change['province_id'], None)
        self.assertEqual(NewsEmail_post_change, halland_mun_obj.name)
        self.assertEqual(response.status_code, 302)


    def test_getting_list_ads_initial_view(self):
        response = self.client.get('/postings/list')
        json_response = json.dumps(response.content.decode("utf-8"))

        self.assertEqual(response.status_code, 200)
        self.assertIn(f'({self.total_count})', json_response) # Number of all ads
        self.assertIn(f'({self.total_offering_count})', json_response) # Number of offering ads
        self.assertIn(f'({self.total_requesting_count})', json_response) # Number of requesting ads

    def test_requesting_first_ten_ads(self):
        
        data = {
            "type_of_ad": "all",
            "province":"---------",
            "municipality":"---------",
            "area":"---------",
            "days_per_week":[],
            "size_offered":[],
            "size_requested":[],
            "offset":0
        }

        json_data = json.dumps(data)

        response = self.client.post(
            '/postings/list', 
            json_data,
            content_type='application/json',
        )

        json_response = json.loads(response.content.decode("utf-8"))
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('"pk": 1', json_response)
        self.assertIn('"pk": 7', json_response)
        self.assertIn('"pk": 10', json_response)
        self.assertNotIn('"pk": 11', json_response)


    def test_requesting_first_ten_ads(self):
            
            data = {
                "type_of_ad": "all",
                "province":"---------",
                "municipality":"---------",
                "area":"---------",
                "days_per_week":[],
                "size_offered":[],
                "size_requested":[],
                "offset":10
            }

            json_data = json.dumps(data)

            response = self.client.post(
                '/postings/list', 
                json_data,
                content_type='application/json',
            )

            json_response = json.loads(response.content.decode("utf-8"))
            
            self.assertEqual(response.status_code, 200)
            self.assertIn('"pk": 11', json_response)
            self.assertIn('"pk": 13', json_response)
            self.assertIn('"pk": 15', json_response)
            self.assertNotIn('"pk": 10', json_response)

    def test_requesting_specific_province(self):
            
            data = {
                "type_of_ad": "all",
                "province":"Halland (0, 0)",
                "municipality":"---------",
                "area":"---------",
                "days_per_week":[],
                "size_offered":[],
                "size_requested":[],
                "offset":0
            }

            json_data = json.dumps(data)

            response = self.client.post(
                '/postings/list', 
                json_data,
                content_type='application/json',
            )

            json_response = json.loads(response.content.decode("utf-8"))
            
            self.assertEqual(response.status_code, 200)
            self.assertIn(f'"pk": {self.user_2_offering_ads_halland_falkenberg[0].pk}', json_response)
            self.assertIn(f'"pk": {self.user_2_offering_ads_halland_halmstad[0].pk}', json_response)
            self.assertIn(f'"pk": {self.user_1_offering_ads_stockholm_stockholms_stad[0].pk}', json_response)


    def test_requesting_specific_municipality(self):
            
            data = {
                "type_of_ad": "all",
                "province":"Halland (0, 0)",
                "municipality":"Falkenberg",
                "area":"---------",
                "days_per_week":[],
                "size_offered":[],
                "size_requested":[],
                "offset":0
            }

            json_data = json.dumps(data)

            response = self.client.post(
                '/postings/list', 
                json_data,
                content_type='application/json',
            )

            json_response = json.loads(response.content.decode("utf-8"))
            
            self.assertEqual(response.status_code, 200)
            self.assertIn(f'"pk": {self.user_2_offering_ads_halland_falkenberg[0].pk}', json_response)
            self.assertNotIn(f'"pk": {self.user_2_offering_ads_halland_halmstad[0].pk}', json_response)


    def test_requesting_specific_area(self):
            
            data = {
                "type_of_ad": "all",
                "province":"Stockholm (0, 0)",
                "municipality":"Stockholms stad",
                "area":"Katarina, Sofia",
                "days_per_week":[],
                "size_offered":[],
                "size_requested":[],
                "offset":0
            }

            json_data = json.dumps(data)

            response = self.client.post(
                '/postings/list', 
                json_data,
                content_type='application/json',
            )

            json_response = json.loads(response.content.decode("utf-8"))
            
            self.assertEqual(response.status_code, 200)
            self.assertIn(f'"pk": {self.user_2_offering_ads_stockholm_stockholms_stad_katarina_sofia[0].pk}', json_response)
            self.assertNotIn(f'"pk": {self.user_2_requesting_ads_sthlm[0].pk}', json_response)


    def test_requesting_all_offering_ads(self):
                
                data = {
                    "type_of_ad": "offering",
                    "province":"---------",
                    "municipality":"---------",
                    "area":"---------",
                    "days_per_week":[],
                    "size_offered":[],
                    "size_requested":[],
                    "offset":0
                }

                json_data = json.dumps(data)

                response = self.client.post(
                    '/postings/list', 
                    json_data,
                    content_type='application/json',
                )

                json_response = json.loads(response.content.decode("utf-8"))
                
                self.assertEqual(response.status_code, 200)
                self.assertIn(f'"pk": {self.user_2_offering_ads_stockholm_stockholms_stad_katarina_sofia[0].pk}', json_response)
                self.assertNotIn(f'"pk": {self.user_2_requesting_ads_sthlm[0].pk}', json_response)
        

    def test_requesting_all_requesting_ads(self):
            
            data = {
                "type_of_ad": "requesting",
                "province":"---------",
                "municipality":"---------",
                "area":"---------",
                "days_per_week":[],
                "size_offered":[],
                "size_requested":[],
                "offset":0
            }

            json_data = json.dumps(data)

            response = self.client.post(
                '/postings/list', 
                json_data,
                content_type='application/json',
            )

            json_response = json.loads(response.content.decode("utf-8"))
            
            self.assertEqual(response.status_code, 200)
            self.assertIn(f'"pk": {self.user_2_requesting_ads_sthlm[0].pk}', json_response)
            self.assertNotIn(f'"pk": {self.user_2_offering_ads_stockholm_stockholms_stad_katarina_sofia[0].pk}', json_response)
            




    


