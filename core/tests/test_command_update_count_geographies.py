from django.core.management import call_command
from django.test import TestCase
import pytz
import datetime

from core.tests.factories import create_offering_ads, create_requesting_ads
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


    def test_offering_ads_count_updates_correctly(cls):

        cls.assertEqual(cls.province.offering_count, 0)
        cls.assertEqual(cls.municipality.offering_count, 0)
        cls.assertEqual(cls.area_1.offering_count, 0)

        ad_1 = create_offering_ads(
            province=cls.province,
            municipality=cls.municipality,
            area=cls.area_1,
            user=cls.user,
            is_published=True,
        )

        ad_1 = create_offering_ads(
            province=cls.province,
            municipality=cls.municipality,
            area=cls.area_2,
            user=cls.user,
            is_published=True,
        )

        result = call_command('update_count_geographies')

        cls.province.refresh_from_db()
        cls.municipality.refresh_from_db()
        cls.area_1.refresh_from_db()
        cls.area_2.refresh_from_db()


        cls.assertEqual(cls.province.offering_count, 2)
        cls.assertEqual(cls.municipality.offering_count, 2)
        cls.assertEqual(cls.area_1.offering_count, 1)
        cls.assertEqual(cls.area_2.offering_count, 1)


    def test_requesting_ads_count_updates_correctly(cls):

        cls.assertEqual(cls.province.requesting_count, 0)
        cls.assertEqual(cls.municipality.requesting_count, 0)
        cls.assertEqual(cls.area_1.requesting_count, 0)

        ad_1 = create_requesting_ads(
            province=cls.province,
            municipality=cls.municipality,
            area=cls.area_1,
            user=cls.user,
            is_published=True,
        )

        ad_1 = create_requesting_ads(
            province=cls.province,
            municipality=cls.municipality,
            area=cls.area_2,
            user=cls.user,
            is_published=True,
        )

        result = call_command('update_count_geographies')

        cls.province.refresh_from_db()
        cls.municipality.refresh_from_db()
        cls.area_1.refresh_from_db()
        cls.area_2.refresh_from_db()


        cls.assertEqual(cls.province.requesting_count, 2)
        cls.assertEqual(cls.municipality.requesting_count, 2)
        cls.assertEqual(cls.area_1.requesting_count, 1)
        cls.assertEqual(cls.area_2.requesting_count, 1)