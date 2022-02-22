import json
from pprint import pprint
import os


from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse

from core.models import Advertisement, DogBreed, Municipality, NewsEmail, Province
from core.tests import factories
from core.forms.ad_forms import OfferingDogForm, RequestingDogForm
from core.abstracts import prevent_request_warnings
from core.views.payment_views import SwishCallback

from django.contrib.auth import get_user_model

User = get_user_model()


TEST_DIR = os.path.dirname(os.path.abspath(__file__))
TEST_DATA_DIR = os.path.join(TEST_DIR, 'data')
test_image_path = os.path.join(TEST_DATA_DIR, 'favicon.png')

class TestSetupPaymentViews(TestCase):
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
        cls.user_1_ad_without_payment = factories.create_ad_without_payment(user=cls.user1)
        cls.user_1_ad_with_initial_payment = factories.create_ad_with_initial_payment(user=cls.user1)
        cls.user_1_ad_with_extended_payment = factories.create_ad_with_extended_payment(user=cls.user1)

        cls.user_2_ad_without_payment = factories.create_ad_without_payment(user=cls.user2)
        cls.user_2_ad_with_initial_payment = factories.create_ad_with_initial_payment(user=cls.user2)
        cls.user_2_ad_with_extended_payment = factories.create_ad_with_initial_payment(user=cls.user2)

        # Swish callback data
        cls.swish_callback_data = {
            'id': 'CD3820D9B3734EFAB4EC2CCA63C66BCB',
            'payeePaymentReference': '3',
            'paymentReference': 'A05B3CFC615143798F9DF8509E39C9B8',
            'callbackUrl': 'https://kontorshund.se/swish/callback',
            'payerAlias': '46721506520',
            'payeeAlias': '1233473337',
            'currency': 'SEK',
            'message': 'Betalning för annons med ID 3',
            'errorMessage': '',
            'status': 'PAID',
            'amount': 1.0,
            'dateCreated': '2022-02-22T19:26:03.619Z',
            'datePaid': '2022-02-22T19:26:14.826Z',
            'errorCode': ''
        }


    #setUp: Run once for every test method to setup clean data.
    def setUp(self):
        pass


class TestPaymentStatus(TestSetupPaymentViews):

    def test_unauthenticated_getting_initial_payment_status(self):
        response = self.client.post(reverse('check_initial_payment_status', kwargs={'pk': self.user_1_ad_with_extended_payment.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/accounts/login/')

    def test_unauthenticated_getting_extended_payment_status(self):
        response = self.client.post(reverse('check_extended_payment_status', kwargs={'pk': self.user_1_ad_with_extended_payment.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/accounts/login/')

    def test_getting_another_users_initial_payment_status(self):
        self.client.login(username=self.username1, password=self.password1)
        response = self.client.post(reverse('check_initial_payment_status', kwargs={'pk': self.user_2_ad_with_initial_payment.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/profile')

    def test_getting_another_users_extended_payment_status(self):
        self.client.login(username=self.username1, password=self.password1)
        response = self.client.post(reverse('check_extended_payment_status', kwargs={'pk': self.user_2_ad_with_extended_payment.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/profile')

    def test_getting_successfull_initial_payment_status(self):
        self.client.login(username=self.username1, password=self.password1)
        response = self.client.post(reverse('check_initial_payment_status', kwargs={'pk': self.user_1_ad_with_initial_payment.pk}))
        response_json = json.loads(response.content)
        self.assertEqual(self.user_1_ad_with_initial_payment.has_initial_payment, True)
        self.assertEqual(response_json, 'Payment is complete!')
        self.assertEqual(response.status_code, 200)

    def test_getting_successfull_extended_payment_status(self):
        self.client.login(username=self.username1, password=self.password1)
        response = self.client.post(reverse('check_extended_payment_status', kwargs={'pk': self.user_1_ad_with_extended_payment.pk}))
        response_json = json.loads(response.content)
        self.assertEqual(self.user_1_ad_with_extended_payment.has_extended_payment, True)
        self.assertEqual(response_json, 'Payment is complete!')
        self.assertEqual(response.status_code, 200)

    @prevent_request_warnings
    def test_getting_missing_initial_payment_status(self):
        self.client.login(username=self.username1, password=self.password1)
        response = self.client.post(reverse('check_initial_payment_status', kwargs={'pk': self.user_1_ad_with_extended_payment.pk}))
        response_json = json.loads(response.content)
        self.assertEqual(self.user_1_ad_with_extended_payment.has_initial_payment, False)
        self.assertEqual(response_json, 'Payment is NOT complete')
        self.assertEqual(response.status_code, 404)

    @prevent_request_warnings
    def test_getting_missing_extended_payment_status(self):
        self.client.login(username=self.username1, password=self.password1)
        response = self.client.post(reverse('check_extended_payment_status', kwargs={'pk': self.user_1_ad_with_initial_payment.pk}))
        response_json = json.loads(response.content)
        self.assertEqual(self.user_1_ad_with_initial_payment.has_extended_payment, False)
        self.assertEqual(response_json, 'Payment is NOT complete')
        self.assertEqual(response.status_code, 404)

    @prevent_request_warnings
    def test_getting_initial_payment_status_for_non_existing_ad(self):
        self.client.login(username=self.username1, password=self.password1)
        response = self.client.post(reverse('check_initial_payment_status', kwargs={'pk': 20}))
        self.assertEqual(response.status_code, 404)

    @prevent_request_warnings
    def test_getting_extended_payment_status_for_non_existing_ad(self):
        self.client.login(username=self.username1, password=self.password1)
        response = self.client.post(reverse('check_extended_payment_status', kwargs={'pk': 20}))
        self.assertEqual(response.status_code, 404)


class TestAndroidPage(TestSetupPaymentViews):

    def test_getting_android_page(self):
        response = self.client.get(reverse('android_success_page'))
        self.assertEqual(response.status_code, 200)


class TestSwishCallbackView(TestSetupPaymentViews):


    def test_status_paid(self):

        request_body_string = json.dumps(self.swish_callback_data)
        request_body_bytes = request_body_string.encode('utf-8')

        request = type('', (), {})()
        request.body = request_body_bytes

        SwishCallback.post(self, request=request)




# check status paid

    # For non existant ad

    # For existant ad

        # With initial payment

            # With deletion date 5 days ahead

            # With deletion date today

        # Without initial payment 


# Check status other