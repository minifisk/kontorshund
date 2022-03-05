from django.core.management import call_command
from django.test import TestCase
import pytz
import datetime

from core.tests.factories import create_offering_ads
from core.models import Province, Municipality, Area

from django.contrib.auth import get_user_model

User = get_user_model()

class TestSendingReminderEmails(TestCase):
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
        cls.six_days_ahead = cls.today + datetime.timedelta(days=6)
        cls.seven_days_ahead = cls.today + datetime.timedelta(days=7)
        cls.eight_days_ahead = cls.today + datetime.timedelta(days=8)


        cls.ad_deletion_date_six_days_ahead = create_offering_ads(
            province=cls.province,
            municipality=cls.municipality,
            user=cls.user,
            is_published=True,
            deletion_date=cls.six_days_ahead,
        )

        cls.ad_deletion_date_seven_days_ahead = create_offering_ads(
            province=cls.province,
            municipality=cls.municipality,
            user=cls.user,
            is_published=True,
            deletion_date=cls.seven_days_ahead,
        )

        cls.ad_deletion_date_eight_days_ahead = create_offering_ads(
            province=cls.province,
            municipality=cls.municipality,
            user=cls.user,
            is_published=True,
            deletion_date=cls.eight_days_ahead,
        )


    def test_only_ads_with_deletion_date_1_week_ahead_gets_email(self):
        result = call_command('send_reminder_1_week_before')

        self.assertNotIn(str(self.ad_deletion_date_six_days_ahead[0].pk), result)
        self.assertIn(str(self.ad_deletion_date_seven_days_ahead[0].pk), result)
        self.assertNotIn(str(self.ad_deletion_date_eight_days_ahead[0].pk), result)