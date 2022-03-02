import json
from pprint import pprint
import os
from venv import create
import datetime
from dateutil.relativedelta import *

from django.core.management import call_command
from django.conf import settings
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from core.models import PaymentKind
from core.tests import factories
from core.abstracts import prevent_request_warnings
from core.views.payment_views import SwishCallback, logger, get_qr_code
from core.tests.factories import create_swish_callback_payload
from core.models import Area

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

        # USERS
        cls.username1 = 'testuser1'
        cls.password1 = '1X<ISRUkw+tuK'

        cls.username2 = 'testuser2'
        cls.password2 = '2HJ1vRV0Z&3iD'

        cls.user1 = User.objects.create_user(username=cls.username1, password=cls.password1)
        cls.user2 = User.objects.create_user(username=cls.username2, password=cls.password2)

        cls.user1.save()
        cls.user2.save()

        cls.user_dict = {}

        from random import randrange
        username = f'asdf {randrange(100)}'
        password = '1234'
            
        User.objects.create_user(username=username, password=password)

        # def create_users(number_of_users=1):
        #     from random import randrange
        #     username = f'asdf {randrange(100)}'
        #     password = '1234'
            
        #     for x in range(number_of_users):
        #         cls.user_dict[x] = User.objects.create_user(username=username, password=password)

        # create_users(number_of_users=1)

        # print(cls.user_dict)

            

        # from core.tests.factories import create_news_email
        # from core.models import Province, Municipality, IntervalChoices, AdTypesChoices
        
        # # SUBSCRIPTIONS
        # cls.province = Province.objects.get(name='Stockholm'),
        # cls.municipality = Municipality.objects.get(name='Stockholms stad'),
        # cls.area = Area.objects.get(name='Enskede, Årsta, Skarpnäck')

        # ##### Offering ######
        # cls.ad_type_offering = AdTypesChoices.OFFERING

        # ### Daily 
        # cls.interval_daily = IntervalChoices.DAILY
        
        # #### subscription without areas
        # cls.news_email_daily_offering_without_area = create_news_email( 
        #     user=cls.user_dict[0],
        #     province=cls.province,
        #     municipality=cls.municipality,
        #     interval=cls.interval_daily,
        #     ad_type=cls.ad_type_offering,
        #     is_active=True
        # )
        
        # #### subscription with areas
        # cls.news_email_daily_offering_with_area = create_news_email( 
        #     user=cls.user_dict[1],
        #     province=cls.province,
        #     municipality=cls.municipality,
        #     interval=cls.interval_daily,
        #     ad_type=cls.ad_type_offering,
        #     is_active=True
        # )

        # cls.news_email_daily_offering_with_area.areas.add(cls.area)

        # ### Weekly 
        # cls.interval_weekly = IntervalChoices.WEEKLY

        # #### subscription without areas
        # cls.news_email_daily_offering_without_area = create_news_email( 
        #     user=cls.user_dict[2],
        #     province=cls.province,
        #     municipality=cls.municipality,
        #     interval=cls.interval_weekly,
        #     ad_type=cls.ad_type_offering,
        #     is_active=True
        # )

        # #### subscription with areas
        # cls.news_email_daily_offering_with_area = create_news_email( 
        #     user=cls.user_dict[3],
        #     province=cls.province,
        #     municipality=cls.municipality,
        #     interval=cls.interval_weekly,
        #     ad_type=cls.ad_type_offering,
        #     is_active=True
        # )

        # cls.news_email_daily_offering_with_area.areas.add(cls.area)


        # ##### Requesting #####
        # cls.ad_type_requesting = AdTypesChoices.REQUESTING

        # #### subscription without areas
        # cls.news_email_daily_offering_without_area = create_news_email( 
        #     user=cls.user_dict[4],
        #     province=cls.province,
        #     municipality=cls.municipality,
        #     interval=cls.interval_daily,
        #     ad_type=cls.ad_type_requesting,
        #     is_active=True
        # )
        
        # #### subscription with areas
        # cls.news_email_daily_offering_with_area = create_news_email( 
        #     user=cls.user_dict[5],
        #     province=cls.province,
        #     municipality=cls.municipality,
        #     interval=cls.interval_daily,
        #     ad_type=cls.ad_type_requesting,
        #     is_active=True
        # )

        # cls.news_email_daily_offering_with_area.areas.add(cls.area)

        # ### Weekly 
        # cls.interval_weekly = IntervalChoices.WEEKLY

        # #### subscription without areas
        # cls.news_email_daily_offering_without_area = create_news_email( 
        #     user=cls.user_dict[6],
        #     province=cls.province,
        #     municipality=cls.municipality,
        #     interval=cls.interval_weekly,
        #     ad_type=cls.ad_type_requesting,
        #     is_active=True
        # )

        # #### subscription with areas
        # cls.news_email_daily_offering_with_area = create_news_email( 
        #     user=cls.user_dict[7],
        #     province=cls.province,
        #     municipality=cls.municipality,
        #     interval=cls.interval_weekly,
        #     ad_type=cls.ad_type_requesting,
        #     is_active=True
        # )

        # cls.news_email_daily_offering_with_area.areas.add(cls.area)





    #setUp: Run once for every test method to setup clean data.
    def setUp(self):
        pass


class TestDailysubscribeEmails(TestSetupCommands):

    def test_test(self):
        result = call_command('daily_subscribe_mails')

        print(result)