import datetime
from dateutil.relativedelta import *
from random import randrange
import pytz

from django.test import TestCase
from django.contrib.auth import get_user_model

from core.models import Area
from core.models import Province, Municipality, IntervalChoices, AdTypesChoices

User = get_user_model()

class SetUpNewsEmailsTesting(TestCase):
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
        cls.area_1 = Area.objects.get(name='Enskede, Årsta, Skarpnäck')
        cls.area_2 = Area.objects.get(name='Hägersten, Liljeholmen')

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
        cls.news_email_daily_offering_with_area.areas.add(cls.area_1)
        cls.news_email_daily_offering_with_area.save()


        ### Weekly 
        cls.interval_weekly = IntervalChoices.WEEKLY

        cls.news_email_weekly_offering_without_area = cls.user_dict['user_2'].news_email
        cls.news_email_weekly_offering_without_area.province = cls.province
        cls.news_email_weekly_offering_without_area.municipality = cls.municipality
        cls.news_email_weekly_offering_without_area.interval = cls.interval_weekly
        cls.news_email_weekly_offering_without_area.ad_type = cls.ad_type_offering
        cls.news_email_weekly_offering_without_area.is_active = True
        cls.news_email_weekly_offering_without_area.save()

        cls.news_email_weekly_offering_with_area = cls.user_dict['user_3'].news_email
        cls.news_email_weekly_offering_with_area.province = cls.province
        cls.news_email_weekly_offering_with_area.municipality = cls.municipality
        cls.news_email_weekly_offering_with_area.interval = cls.interval_weekly
        cls.news_email_weekly_offering_with_area.ad_type = cls.ad_type_offering
        cls.news_email_weekly_offering_with_area.is_active = True
        cls.news_email_weekly_offering_with_area.areas.add(cls.area_1)
        cls.news_email_weekly_offering_with_area.save()






        ###### Requesting #####
        cls.ad_type_requesting = AdTypesChoices.REQUESTING

        ### Daily 
        cls.interval_daily = IntervalChoices.DAILY

        cls.news_email_daily_requesting_without_area = cls.user_dict['user_4'].news_email
        cls.news_email_daily_requesting_without_area.province = cls.province
        cls.news_email_daily_requesting_without_area.municipality = cls.municipality
        cls.news_email_daily_requesting_without_area.interval = cls.interval_daily
        cls.news_email_daily_requesting_without_area.ad_type = cls.ad_type_requesting
        cls.news_email_daily_requesting_without_area.is_active = True
        cls.news_email_daily_requesting_without_area.save()

        cls.news_email_daily_requesting_with_area = cls.user_dict['user_5'].news_email
        cls.news_email_daily_requesting_with_area.province = cls.province
        cls.news_email_daily_requesting_with_area.municipality = cls.municipality
        cls.news_email_daily_requesting_with_area.interval = cls.interval_daily
        cls.news_email_daily_requesting_with_area.ad_type = cls.ad_type_requesting
        cls.news_email_daily_requesting_with_area.is_active = True
        cls.news_email_daily_requesting_with_area.areas.add(cls.area_1)
        cls.news_email_daily_requesting_with_area.save()

        # ### Weekly 
        cls.interval_weekly = IntervalChoices.WEEKLY

        cls.news_email_weekly_requesting_without_area = cls.user_dict['user_6'].news_email
        cls.news_email_weekly_requesting_without_area.province = cls.province
        cls.news_email_weekly_requesting_without_area.municipality = cls.municipality
        cls.news_email_weekly_requesting_without_area.interval = cls.interval_weekly
        cls.news_email_weekly_requesting_without_area.ad_type = cls.ad_type_requesting
        cls.news_email_weekly_requesting_without_area.is_active = True
        cls.news_email_weekly_requesting_without_area.save()

        cls.news_email_weekly_requesting_with_area = cls.user_dict['user_7'].news_email
        cls.news_email_weekly_requesting_with_area.province = cls.province
        cls.news_email_weekly_requesting_with_area.municipality = cls.municipality
        cls.news_email_weekly_requesting_with_area.interval = cls.interval_weekly
        cls.news_email_weekly_requesting_with_area.ad_type = cls.ad_type_requesting
        cls.news_email_weekly_requesting_with_area.is_active = True
        cls.news_email_weekly_requesting_with_area.areas.add(cls.area_1)
        cls.news_email_weekly_requesting_with_area.save()


        # Time
        utc_sthlm=pytz.timezone('Europe/Stockholm')
        one_hour_back_no_tz = datetime.datetime.now() - datetime.timedelta(hours=1)
        cls.one_hour_back = utc_sthlm.localize(one_hour_back_no_tz) 

        utc_sthlm=pytz.timezone('Europe/Stockholm')
        twenty_three_hours_back_no_tz = datetime.datetime.now() - datetime.timedelta(hours=23)
        cls.twenty_three_hours_back = utc_sthlm.localize(twenty_three_hours_back_no_tz) 

        utc_sthlm=pytz.timezone('Europe/Stockholm')
        twenty_five_hours_back_no_tz = datetime.datetime.now() - datetime.timedelta(days=1, hours=1)
        cls.twenty_five_hours_back = utc_sthlm.localize(twenty_five_hours_back_no_tz) 


    #setUp: Run once for every test method to setup clean data.
    def setUp(self):
        pass

