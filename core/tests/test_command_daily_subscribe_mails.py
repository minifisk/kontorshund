import json
from pprint import pprint
import os
from venv import create
import datetime
from dateutil.relativedelta import *
from random import randrange

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
from core.tests.factories import create_news_email
from core.models import Province, Municipality, IntervalChoices, AdTypesChoices

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


    def create_users(cls, number_of_users=1):
        cls.user_dict = {}
        for i in range(number_of_users):
            username = f'asdf {randrange(10000)}'
            password = '1234'
            cls.user_dict[f'user_{i}'] = User.objects.create_user(username=username, password=password)

    #setUpTestData: Run once to set up non-modified data for all class methods.
    @classmethod
    def setUpTestData(cls):

        # USERS
        cls.create_users(cls, number_of_users=8)
        
        # SUBSCRIPTIONS
        cls.province = Province.objects.get(name='Stockholm')
        cls.municipality = Municipality.objects.get(name='Stockholms stad')
        cls.area = Area.objects.get(name='Enskede, Årsta, Skarpnäck')

        ##### Offering ######
        cls.ad_type_offering = AdTypesChoices.OFFERING

        ### Daily 
        cls.interval_daily = IntervalChoices.DAILY
        
        cls.news_email_daily_offering_without_area = cls.user_dict['user_0'].news_email
        cls.news_email_daily_offering_without_area.province = cls.province
        cls.news_email_daily_offering_without_area.municipality = cls.municipality
        cls.news_email_daily_offering_without_area.interval = cls.interval_daily
        cls.news_email_daily_offering_without_area.ad_type = cls.ad_type_offering
        cls.news_email_daily_offering_without_area.is_active = True
        cls.news_email_daily_offering_without_area.save()

        cls.news_email_daily_offering_with_area = cls.user_dict['user_1'].news_email
        cls.news_email_daily_offering_with_area.province = cls.province
        cls.news_email_daily_offering_with_area.municipality = cls.municipality
        cls.news_email_daily_offering_with_area.interval = cls.interval_daily
        cls.news_email_daily_offering_with_area.ad_type = cls.ad_type_offering
        cls.news_email_daily_offering_with_area.is_active = True
        cls.news_email_daily_offering_with_area.areas.add(cls.area)
        cls.news_email_daily_offering_with_area.save()

        ### Weekly 
        cls.interval_weekly = IntervalChoices.WEEKLY

        cls.news_email_daily_offering_without_area = cls.user_dict['user_2'].news_email
        cls.news_email_daily_offering_without_area.province = cls.province
        cls.news_email_daily_offering_without_area.municipality = cls.municipality
        cls.news_email_daily_offering_without_area.interval = cls.interval_weekly
        cls.news_email_daily_offering_without_area.ad_type = cls.ad_type_offering
        cls.news_email_daily_offering_without_area.is_active = True
        cls.news_email_daily_offering_without_area.save()

        cls.news_email_daily_offering_with_area = cls.user_dict['user_3'].news_email
        cls.news_email_daily_offering_with_area.province = cls.province
        cls.news_email_daily_offering_with_area.municipality = cls.municipality
        cls.news_email_daily_offering_with_area.interval = cls.interval_weekly
        cls.news_email_daily_offering_with_area.ad_type = cls.ad_type_offering
        cls.news_email_daily_offering_with_area.is_active = True
        cls.news_email_daily_offering_with_area.areas.add(cls.area)
        cls.news_email_daily_offering_with_area.save()

        ###### Requesting #####
        cls.ad_type_requesting = AdTypesChoices.REQUESTING

        ### Daily 
        cls.news_email_daily_offering_without_area = cls.user_dict['user_4'].news_email
        cls.news_email_daily_offering_without_area.province = cls.province
        cls.news_email_daily_offering_without_area.municipality = cls.municipality
        cls.news_email_daily_offering_without_area.interval = cls.interval_daily
        cls.news_email_daily_offering_without_area.ad_type = cls.ad_type_requesting
        cls.news_email_daily_offering_without_area.is_active = True
        cls.news_email_daily_offering_without_area.save()

        cls.news_email_daily_offering_with_area = cls.user_dict['user_5'].news_email
        cls.news_email_daily_offering_with_area.province = cls.province
        cls.news_email_daily_offering_with_area.municipality = cls.municipality
        cls.news_email_daily_offering_with_area.interval = cls.interval_daily
        cls.news_email_daily_offering_with_area.ad_type = cls.ad_type_requesting
        cls.news_email_daily_offering_with_area.is_active = True
        cls.news_email_daily_offering_with_area.areas.add(cls.area)
        cls.news_email_daily_offering_with_area.save()

        # ### Weekly 
        cls.interval_weekly = IntervalChoices.WEEKLY

        cls.news_email_daily_offering_without_area = cls.user_dict['user_6'].news_email
        cls.news_email_daily_offering_without_area.province = cls.province
        cls.news_email_daily_offering_without_area.municipality = cls.municipality
        cls.news_email_daily_offering_without_area.interval = cls.interval_weekly
        cls.news_email_daily_offering_without_area.ad_type = cls.ad_type_requesting
        cls.news_email_daily_offering_without_area.is_active = True
        cls.news_email_daily_offering_without_area.save()

        cls.news_email_daily_offering_with_area = cls.user_dict['user_7'].news_email
        cls.news_email_daily_offering_with_area.province = cls.province
        cls.news_email_daily_offering_with_area.municipality = cls.municipality
        cls.news_email_daily_offering_with_area.interval = cls.interval_weekly
        cls.news_email_daily_offering_with_area.ad_type = cls.ad_type_requesting
        cls.news_email_daily_offering_with_area.is_active = True
        cls.news_email_daily_offering_with_area.areas.add(cls.area)
        cls.news_email_daily_offering_with_area.save()


        # Ads
        import pytz
        utc_sthlm=pytz.timezone('Europe/Stockholm')
        one_hour_back_no_tz = datetime.datetime.now() - datetime.timedelta(hours=1)
        one_hour_back = utc_sthlm.localize(one_hour_back_no_tz) 

        print(one_hour_back_no_tz)
        print(one_hour_back)

        from core.tests.factories import create_offering_ad
        
        cls.offering_ad_no_areas = create_offering_ad(
            province=cls.province,
            municipality=cls.municipality,
            user=cls.user_dict['user_1'],
            is_published=True,
            created_at=one_hour_back,
            

        )



    #setUp: Run once for every test method to setup clean data.
    def setUp(self):
        pass


class TestDailysubscribeEmails(TestSetupCommands):

    def test_test(self):
        result = call_command('daily_subscribe_mails')

        print(result)