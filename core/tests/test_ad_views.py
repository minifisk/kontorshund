
import json
from pprint import pprint
import os


from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse

from core.models import Advertisement, DogBreed, Municipality, NewsEmail, Province
from core.tests import factories
from core.forms.ad_forms import OfferingDogForm, RequestingDogForm

from django.contrib.auth import get_user_model

User = get_user_model()


TEST_DIR = os.path.dirname(os.path.abspath(__file__))
TEST_DATA_DIR = os.path.join(TEST_DIR, 'data')
test_image_path = os.path.join(TEST_DATA_DIR, 'favicon.jpeg')

class TestSetupListAndCreate(TestCase):
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
        cls.user_1_offering_ads_stockholm_stockholms_stad = factories.create_offering_adss_stockholm_stockholms_stad(count=cls.count_offering_stockholm_stockholms_stad, user=cls.user1, is_published=True)
        cls.user_2_requesting_ads_sthlm = factories.create_requesting_ads_stockholm_stockholms_stad(count=cls.count_requesting_stockholm_stockholms_stad, user=cls.user2, is_published=True)
       
        cls.user_2_offering_ads_halland_falkenberg = factories.create_offering_adss_halland_falkenberg(count=cls.count_offering_halland_falkenberg, user=cls.user2, is_published=True)
        cls.user_2_offering_ads_halland_halmstad = factories.create_offering_adss_halland_halmstad(count=cls.count_offering_halland_halmstad, user=cls.user2, is_published=True)
        
        cls.user_2_offering_ads_stockholm_stockholms_stad_katarina_sofia = factories.create_offering_adss_stockholm_stockholm_stad_katarina_sofia(count=cls.count_offering_stockholm_stockholms_stad_katarina_sofia, user=cls.user2, is_published=True)


    #setUp: Run once for every test method to setup clean data.
    def setUp(self):
        pass


class TestSetupUpdateAndDelete(TestCase):
    
    fixtures = [
        '/home/dockeruser/web/core/fixtures/breeds.json', 
        '/home/dockeruser/web/core/fixtures/geographies.json', 
        '/home/dockeruser/web/core/fixtures/size_choices.json'
    ]

    #setUpTestData: Run once to set up non-modified data for all class methods.
    @classmethod
    def setUpTestData(cls):

        cls.username1 = 'testuser1'
        cls.password1 = '1X<ISRUkw+tuK'

        cls.username2 = 'testuser2'
        cls.password2 = '2HJ1vRV0Z&3iD'

        cls.user1 = User.objects.create_user(username=cls.username1, password=cls.password1)
        cls.user1.save()

        cls.user2 = User.objects.create_user(username=cls.username2, password=cls.password2)
        cls.user2.save()

        cls.user_1_requesting_ads = factories.create_requesting_ads_stockholm_stockholms_stad(count=1, user=cls.user1, is_published=True)
        cls.user_1_offering_ads = factories.create_offering_adss_stockholm_stockholms_stad(count=1, user=cls.user1, is_published=True)
        cls.user_2_offering_ads = factories.create_offering_adss_stockholm_stockholms_stad(count=1, user=cls.user2, is_published=True)

   
    #setUp: Run once for every test method to setup clean data.
    def setUp(self):
        pass



class TestProfileAndChooseAd(TestSetupListAndCreate):

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
            'interval': ['DL'], 
            'ad_type': ['RQ']
            }

        response = self.client.post('/profile', data)

        NewsEmail_post_change = NewsEmail.objects.get(user__pk=self.user1.pk).municipality.name

        self.assertEqual(NewsEmail_pre_change['province_id'], None)
        self.assertEqual(NewsEmail_post_change, halland_mun_obj.name)
        self.assertEqual(response.status_code, 302)

    def test_choosing_ad_view(self):
  
        self.client.login(username=self.username1, password=self.password1)
        response = self.client.get('/ads/choose')
 
        content = response.content.decode("utf-8")
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('requesting_dog.jpg', content)


class TestListAdsView(TestSetupListAndCreate):

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


class TestCreateOfferingDogView(TestSetupListAndCreate):

    def test_unauthenticated_creating_new_ad_offering(self):
        response = self.client.post('/ads/create/offering-dog')
        self.assertEqual(response.status_code, 302)

    def test_required_fields_in_offering_dog_view(self):
        self.client.login(username=self.username1, password=self.password1)
        response = self.client.post('/ads/create/offering-dog')
        self.assertFormError(response, 'form', 'province', 'This field is required.')
        self.assertFormError(response, 'form', 'municipality', 'This field is required.')
        self.assertFormError(response, 'form', 'hundras', 'This field is required.')
        self.assertFormError(response, 'form', 'image1', 'This field is required.')
        self.assertFormError(response, 'form', 'days_per_week', 'This field is required.')
        self.assertFormError(response, 'form', 'title', 'This field is required.')
        self.assertFormError(response, 'form', 'description', 'This field is required.')
        self.assertFormError(response, 'form', 'size_offered', 'This field is required.')
        self.assertFormError(response, 'form', 'age', 'This field is required.')
        self.assertFormError(response, 'form', 'name', 'This field is required.')

    def test_offering_endpoint_not_containing_requesting_fields(self):
        self.client.login(username=self.username1, password=self.password1)
        response = self.client.post('/ads/create/offering-dog')
        string_ = response.content.decode('utf-8')
        self.assertNotIn('size_requested', string_)


    def test_form_creating_new_ad_offering_dog(self):

        form_data = {
            'province': 1,
            'municipality': 1,
            'age': 3,
            'days_per_week': '1-2',
            'description': 'asdf',
            'title': 'asdf',
            'name': 'roffe',
            'payment_choice': 'S',
            'hundras': 1,
            'size_offered': 1,
        }

        with open(test_image_path, 'rb') as f:
            offering_dog_form = OfferingDogForm(data=form_data, files={'image1': SimpleUploadedFile('image1.png', f.read())})
            self.assertTrue(offering_dog_form.is_valid())


class TestCreateRequestingDogView(TestSetupListAndCreate):

    def test_unauthenticated_creating_new_ad_requesting(self):
        response = self.client.post('/ads/create/requesting-dog')
        self.assertEqual(response.status_code, 302)

    def test_required_fields_in_requesting_dog_view(self):
        self.client.login(username=self.username1, password=self.password1)
        response = self.client.post('/ads/create/requesting-dog')
        self.assertFormError(response, 'form', 'province', 'This field is required.')
        self.assertFormError(response, 'form', 'municipality', 'This field is required.')
        self.assertFormError(response, 'form', 'image1', 'This field is required.')
        self.assertFormError(response, 'form', 'days_per_week', 'This field is required.')
        self.assertFormError(response, 'form', 'title', 'This field is required.')
        self.assertFormError(response, 'form', 'description', 'This field is required.')
        self.assertFormError(response, 'form', 'size_requested', 'This field is required.')

    def test_create_requesting_dog_endpoint_not_containing_offering_fields(self):
        self.client.login(username=self.username1, password=self.password1)
        response = self.client.post('/ads/create/requesting-dog')
        string_ = response.content.decode('utf-8')
        self.assertNotIn('hundras', string_)
        self.assertNotIn('size_offered', string_)

    def test_form_creating_new_ad_requesting_dog(self):

        form_data = {
            'province': 1,
            'municipality': 1,
            'days_per_week': '1-2',
            'description': 'asdf',
            'title': 'asdf',
            'payment_choice': 'S',
            'size_requested': [1],
        }

        with open(test_image_path, 'rb') as f:
            offering_dog_form = RequestingDogForm(data=form_data, files={'image1': SimpleUploadedFile('image1.png', f.read())})            
            self.assertTrue(offering_dog_form.is_valid())


class TestUpdateOfferingDogView(TestSetupUpdateAndDelete):

    def test_required_fields_in_update_offering_dog_view(self):
        self.client.login(username=self.username1, password=self.password1)
        ad = self.user_1_offering_ads[0]
        response = self.client.post(reverse('update_ad_offering_dog', kwargs={'pk': ad.pk}),)
        self.assertFormError(response, 'form', 'province', 'This field is required.')
        self.assertFormError(response, 'form', 'municipality', 'This field is required.')
        self.assertFormError(response, 'form', 'hundras', 'This field is required.')
        self.assertFormError(response, 'form', 'image1', 'This field is required.')
        self.assertFormError(response, 'form', 'days_per_week', 'This field is required.')
        self.assertFormError(response, 'form', 'title', 'This field is required.')
        self.assertFormError(response, 'form', 'description', 'This field is required.')
        self.assertFormError(response, 'form', 'size_offered', 'This field is required.')
        self.assertFormError(response, 'form', 'age', 'This field is required.')
        self.assertFormError(response, 'form', 'name', 'This field is required.')


    def test_get_request_form_for_offering_ad_belonging_to_other_users_ad(self):
        self.client.login(username=self.username2, password=self.password2)
        other_users_ad = self.user_1_offering_ads[0]

        response = self.client.get(reverse('update_ad_offering_dog', kwargs={'pk': other_users_ad.pk}))
        
        self.assertEqual(response.status_code, 302)

    def test_post_request_form_for_offering_ad_belonging_to_other_users_ad(self):
        self.client.login(username=self.username2, password=self.password2)
        other_users_ad = self.user_1_offering_ads[0]

        response = self.client.post(reverse('update_ad_offering_dog', kwargs={'pk': other_users_ad.pk}))
        
        self.assertEqual(response.status_code, 302)

    def test_update_offering_dog_endpoint_not_containing_requesting_fields(self):
        self.client.login(username=self.username1, password=self.password1)
        own_ad = self.user_1_requesting_ads[0]
        response = self.client.post(reverse('update_ad_offering_dog', kwargs={'pk': own_ad.pk}))
        string_ = response.content.decode('utf-8')
        self.assertNotIn('size_requested', string_)

    def test_post_request_offering_dog_view(self):
        self.client.login(username=self.username1, password=self.password1)
        own_ad = self.user_1_offering_ads[0]

        self.assertEqual(own_ad.author.username, self.username1)

        with open(test_image_path, 'rb') as f:

            new_title = 'New title'

            form_data = {
                'province': 1,
                'municipality': 1,
                'age': 3,
                'days_per_week': '1-2',
                'description': 'asdf',
                'title': new_title,
                'name': 'roffe',
                'payment_choice': 'S',
                'hundras': 1,
                'size_offered': 1,
                'image1': SimpleUploadedFile('image1.png', f.read())
            }

            response = self.client.post(reverse('update_ad_offering_dog', kwargs={'pk': own_ad.pk}), form_data)

            self.assertEqual(own_ad.title, own_ad.title)
            own_ad.refresh_from_db()
            self.assertEqual(own_ad.title, new_title)

            self.assertEqual(response.status_code, 302)

    
class TestUpdateRequestingDogView(TestSetupUpdateAndDelete):

    def test_required_fields_in_update_requesting_dog_view(self):
        self.client.login(username=self.username1, password=self.password1)
        first_ad = self.user_1_requesting_ads[0]
        response = self.client.post(reverse('update_ad_requesting_dog', kwargs={'pk': first_ad.pk}),)
        self.assertFormError(response, 'form', 'province', 'This field is required.')
        self.assertFormError(response, 'form', 'municipality', 'This field is required.')
        self.assertFormError(response, 'form', 'image1', 'This field is required.')
        self.assertFormError(response, 'form', 'days_per_week', 'This field is required.')
        self.assertFormError(response, 'form', 'title', 'This field is required.')
        self.assertFormError(response, 'form', 'description', 'This field is required.')
        self.assertFormError(response, 'form', 'size_requested', 'This field is required.')

    def test_get_request_form_for_requesting_ad_belonging_to_other_users_ad(self):
        self.client.login(username=self.username2, password=self.password2)
        other_users_ad = self.user_1_requesting_ads[0]
        response = self.client.get(reverse('update_ad_requesting_dog', kwargs={'pk': other_users_ad.pk}))
        self.assertEqual(response.status_code, 302)

    def test_post_request_form_for_requesting_ad_belonging_to_other_users_ad(self):
        self.client.login(username=self.username2, password=self.password2)
        other_users_ad = self.user_1_requesting_ads[0]
        response = self.client.post(reverse('update_ad_requesting_dog', kwargs={'pk': other_users_ad.pk}))
        self.assertEqual(response.status_code, 302)

    def test_update_requesting_dog_endpoint_not_containing_offering_fields(self):
        self.client.login(username=self.username1, password=self.password1)
        own_ad = self.user_1_requesting_ads[0]
        response = self.client.post(reverse('update_ad_requesting_dog', kwargs={'pk': own_ad.pk}))
        string_ = response.content.decode('utf-8')
        self.assertNotIn('hundras', string_)
        self.assertNotIn('size_offered', string_)

    def test_post_request_offering_dog_view(self):
        self.client.login(username=self.username1, password=self.password1)
        own_ad = self.user_1_offering_ads[0]

        self.assertEqual(own_ad.author.username, self.username1)

        with open(test_image_path, 'rb') as f:

            new_title = 'New title'

            form_data = {
                'province': 1,
                'municipality': 1,
                'age': 3,
                'days_per_week': '1-2',
                'description': 'asdf',
                'title': new_title,
                'payment_choice': 'S',
                'size_requested': [1],
                'image1': SimpleUploadedFile('image1.png', f.read())
            }

            response = self.client.post(reverse('update_ad_requesting_dog', kwargs={'pk': own_ad.pk}), form_data)

            self.assertEqual(own_ad.title, own_ad.title)
            own_ad.refresh_from_db()
            self.assertEqual(own_ad.title, new_title)

            self.assertEqual(response.status_code, 302)


class TestAdDetailView(TestSetupUpdateAndDelete):

    def test_ad_detail_view(self):
        user_1_ad = self.user_1_requesting_ads[0]
        response = self.client.get(reverse('ad_detail', kwargs={'pk': user_1_ad.pk}),)
        
        response_string = response.content.decode('utf-8')

        self.assertIn(user_1_ad.title, response_string)
        self.assertIn(user_1_ad.province.name, response_string)
        self.assertIn(user_1_ad.municipality.name, response_string)
        self.assertEqual(response.status_code, 200)


class TestAdDeleteView(TestSetupUpdateAndDelete):

    def test_delete_ad_view_unauthenticated(self):
        user_1_ad = self.user_1_requesting_ads[0]
        response = self.client.post(reverse('delete_ad', kwargs={'pk': user_1_ad.pk}),)
        self.assertEqual(response.status_code, 302)
            
    def test_delete_ad_view_other_users_ad(self):
        self.client.login(username=self.username1, password=self.password1)
        user_2_ad = self.user_2_offering_ads[0]
        response = self.client.post(reverse('delete_ad', kwargs={'pk': user_2_ad.pk}),)
        self.assertEqual(response.status_code, 302)

    # def test_delete_ad(self):
    #     self.client.login(username=self.username1, password=self.password1)
    #     user_1_ad = self.user_1_offering_ads[0]
    #     response = self.client.delete(reverse('delete_ad', kwargs={'pk': user_1_ad.pk}),)
    #     user_1_ad.refresh_from_db()
    #     #self.assertEqual(response.status_code, 302)






    


