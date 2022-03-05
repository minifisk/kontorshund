from django.core.management import call_command
from django.test import TestCase
import pytz
import datetime

from core.tests.factories import create_offering_ads
from core.models import Province, Municipality, Area

from django.contrib.auth import get_user_model

User = get_user_model()

class TestDeactivationOfAdsRunningOutOfTime(TestCase):
    fixtures = [
        '/home/dockeruser/web/core/fixtures/breeds.json', 
        '/home/dockeruser/web/core/fixtures/geographies.json', 
        '/home/dockeruser/web/core/fixtures/size_choices.json'
    ]
    
    def setUp(cls):
        
        cls.user = User.objects.create(email='test@test.se')
        cls.province = Province.objects.get(name='Stockholm')
        cls.municipality = Municipality.objects.get(name='Stockholms stad')
        cls.area_1 = Area.objects.get(name='Enskede, Årsta, Skarpnäck')
        cls.area_2 = Area.objects.get(name='Hägersten, Liljeholmen')
        
        cls.today = datetime.datetime.now(pytz.timezone('Europe/Stockholm')).date()
        cls.yesterday = cls.today - datetime.timedelta(days=1)
        cls.tomorrow = cls.today + datetime.timedelta(days=1)

        cls.ad_deletion_date_today = create_offering_ads(
            province=cls.province,
            municipality=cls.municipality,
            user=cls.user,
            is_published=True,
            deletion_date=cls.today,
        )

        cls.ad_deletion_date_yesterday = create_offering_ads(
            province=cls.province,
            municipality=cls.municipality,
            user=cls.user,
            is_published=True,
            deletion_date=cls.yesterday,
        )

        cls.ad_deletion_date_tomorrow = create_offering_ads(
            province=cls.province,
            municipality=cls.municipality,
            user=cls.user,
            is_published=True,
            deletion_date=cls.tomorrow,
        )


    def test_only_ads_with_deletion_date_today_or_earlier_gets_deleted(self):
        result = call_command('deactivate_ads_on_deletion_date')

        self.assertEqual(self.ad_deletion_date_yesterday[0].is_deleted, False)
        self.assertEqual(self.ad_deletion_date_today[0].is_deleted, False)
        self.assertEqual(self.ad_deletion_date_tomorrow[0].is_deleted, False)


        self.assertIn(str(self.ad_deletion_date_yesterday[0].pk), result)
        self.assertIn(str(self.ad_deletion_date_today[0].pk), result)
        self.assertNotIn(str(self.ad_deletion_date_tomorrow[0].pk), result)

        self.ad_deletion_date_yesterday[0].refresh_from_db()
        self.ad_deletion_date_today[0].refresh_from_db()
        self.ad_deletion_date_tomorrow[0].refresh_from_db()

        self.assertEqual(self.ad_deletion_date_yesterday[0].is_deleted, True)
        self.assertEqual(self.ad_deletion_date_today[0].is_deleted, True)
        self.assertEqual(self.ad_deletion_date_tomorrow[0].is_deleted, False)