import json
from pprint import pprint
import os
from venv import create
import datetime
from dateutil.relativedelta import *



from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse

from core.models import PaymentKind
from core.tests import factories
from core.forms.ad_forms import OfferingDogForm, RequestingDogForm
from core.abstracts import prevent_request_warnings
from core.views.payment_views import SwishCallback
from core.tests.factories import create_swish_callback_payload

from django.contrib.auth import get_user_model
from core.views.payment_views import logger


User = get_user_model()


TEST_DIR = os.path.dirname(os.path.abspath(__file__))
TEST_DATA_DIR = os.path.join(TEST_DIR, 'data')
test_image_path = os.path.join(TEST_DATA_DIR, 'favicon.jpeg')

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

        cls.one_week_ago = datetime.date.today() - datetime.timedelta(days=7)
        cls.one_week_ahead = datetime.date.today() + datetime.timedelta(days=7)
        cls.one_week_and_one_month_ahead = cls.one_week_ahead + relativedelta(months=+1)


        cls.user_1_ad_with_initial_payment_deletion_date_one_week_ago = factories.create_ad_with_initial_payment(
            user=cls.user1,
            deletion_date=cls.one_week_ago
            )

        cls.user_1_ad_with_initial_payment_deletion_date_one_week_ahead = factories.create_ad_with_initial_payment(
            user=cls.user1,
            deletion_date=cls.one_week_ahead
            )

        cls.user_2_ad_without_payment = factories.create_ad_without_payment(user=cls.user2)
        cls.user_2_ad_with_initial_payment = factories.create_ad_with_initial_payment(user=cls.user2)
        cls.user_2_ad_with_extended_payment = factories.create_ad_with_initial_payment(user=cls.user2)




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


    def test_ad_without_payment_creates_initial_payment(self):

        payment_before_request = self.user_1_ad_without_payment.payment_set.all()

        self.assertEqual(self.user_1_ad_without_payment.is_published, False)
        self.assertEqual(payment_before_request.exists(), False)
        
        swish_payload = create_swish_callback_payload(self, ad_id=self.user_1_ad_without_payment.pk)
        
        request_body_string = json.dumps(swish_payload)
        request_body_bytes = request_body_string.encode('utf-8')
        request = type('', (), {})()
        request.body = request_body_bytes
        
        SwishCallback.post(self, request=request)

        payment_after_request = self.user_1_ad_without_payment.payment_set.all()
        
        self.user_1_ad_without_payment.refresh_from_db()

        self.assertEqual(self.user_1_ad_without_payment.is_published, True)
        self.assertEqual(payment_after_request.exists(), True)


    def test_ad_with_initial_payment_creates_extended_payment(self):

        payment_before_request_qs = self.user_1_ad_with_initial_payment.payment_set.all()
        initial_payment_exists = payment_before_request_qs.filter(payment_kind=PaymentKind.INITIAL).exists()
        extended_payment_dont_exist = payment_before_request_qs.filter(payment_kind=PaymentKind.EXTENDED).exists()

        self.assertEqual(payment_before_request_qs.count(), 1)
        self.assertEqual(initial_payment_exists, True)
        self.assertEqual(extended_payment_dont_exist, False)

        swish_payload = create_swish_callback_payload(self, ad_id=self.user_1_ad_with_initial_payment.pk)
        
        request_body_string = json.dumps(swish_payload)
        request_body_bytes = request_body_string.encode('utf-8')
        request = type('', (), {})()
        request.body = request_body_bytes
        
        SwishCallback.post(self, request=request)

        payment_after_request_qs = self.user_1_ad_with_initial_payment.payment_set.all()
        initial_payment_exists = payment_before_request_qs.filter(payment_kind=PaymentKind.INITIAL).exists()
        extended_payment_exist = payment_before_request_qs.filter(payment_kind=PaymentKind.EXTENDED).exists()

        self.assertEqual(payment_after_request_qs.count(), 2)
        self.assertEqual(initial_payment_exists, True)
        self.assertEqual(extended_payment_exist, True)

    
    def test_payload_not_being_paid(self):

        swish_payload = create_swish_callback_payload(
            self, 
            ad_id=self.user_1_ad_with_initial_payment.pk,
            status='ERROR'
            )
        
        request_body_string = json.dumps(swish_payload)
        request_body_bytes = request_body_string.encode('utf-8')
        request = type('', (), {})()
        request.body = request_body_bytes
        
        with self.assertLogs(logger=logger, level='ERROR') as cm:
            SwishCallback.post(self, request=request)

            self.assertIn(
                "Problem creating payment",
                cm.output[0]
            )
        

 
    def test_non_existant_ad(self):

        swish_payload = create_swish_callback_payload(
            self, 
            ad_id=100
        )
        
        request_body_string = json.dumps(swish_payload)
        request_body_bytes = request_body_string.encode('utf-8')
        request = type('', (), {})()
        request.body = request_body_bytes
        
        with self.assertLogs(logger=logger, level='ERROR') as cm:
            response = SwishCallback.post(self, request=request)
            
            self.assertEqual(response.status_code, 404)

            self.assertIn(
                "Ad could not be found in Swish callback view",
                cm.output[0]
            )



    def test_ad_with_deletion_date_last_week_still_gets_date_one_month_ahead_from_today(self):
   
        swish_payload = create_swish_callback_payload(self, ad_id=self.user_1_ad_with_initial_payment_deletion_date_one_week_ago.pk)
        
        self.assertEqual(self.user_1_ad_with_initial_payment_deletion_date_one_week_ago.deletion_date, self.one_week_ago)

        request_body_string = json.dumps(swish_payload)
        request_body_bytes = request_body_string.encode('utf-8')
        request = type('', (), {})()
        request.body = request_body_bytes

        SwishCallback.post(self, request=request)

        self.user_1_ad_with_initial_payment_deletion_date_one_week_ago.refresh_from_db()
        one_month_ahead = datetime.date.today() + relativedelta(months=+1)
        self.assertEqual(self.user_1_ad_with_initial_payment_deletion_date_one_week_ago.deletion_date, one_month_ahead)



    def test_ad_with_deletion_date_one_week_ahead_gets_deletion_date_one_month_from_that_date(self):
   
        swish_payload = create_swish_callback_payload(self, ad_id=self.user_1_ad_with_initial_payment_deletion_date_one_week_ahead.pk)

        self.assertEqual(self.user_1_ad_with_initial_payment_deletion_date_one_week_ahead.deletion_date, self.one_week_ahead)
        
        request_body_string = json.dumps(swish_payload)
        request_body_bytes = request_body_string.encode('utf-8')
        request = type('', (), {})()
        request.body = request_body_bytes

        SwishCallback.post(self, request=request)

        self.user_1_ad_with_initial_payment_deletion_date_one_week_ahead.refresh_from_db()

        self.assertEqual(self.user_1_ad_with_initial_payment_deletion_date_one_week_ahead.deletion_date, self.one_week_and_one_month_ahead)

