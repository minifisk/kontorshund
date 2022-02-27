import json
from pprint import pprint
import os
from venv import create
import datetime
from dateutil.relativedelta import *


from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from core.models import PaymentKind
from core.tests import factories
from core.abstracts import prevent_request_warnings
from core.views.payment_views import SwishCallback, logger, get_qr_code
from core.tests.factories import create_swish_callback_payload
from django.conf import settings

from kontorshund.settings import PRICE_SWISH_INITIAL, PRICE_SWISH_EXTEND


User = get_user_model()

# Set-up for imagefile in tests
TEST_DIR = os.path.dirname(os.path.abspath(__file__))
TEST_DATA_DIR = os.path.join(TEST_DIR, 'data')
test_image_path = os.path.join(TEST_DATA_DIR, 'favicon.jpeg')

class TestSetupCommands(TestCase):
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


        # Offering-  Daily subscription with areas
        

        # Offering - Daily subscription without areas


        # Requesting - Weekly subscription with areas

        # Requesting - Weekly subscription without areas










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


class TestPaymentStatus(TestSetupCommands):

    def test_test(self):
        pass