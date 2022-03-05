from core.tests import common_set_up_classes
from django.core.management import call_command

from core.tests.factories import create_offering_ads, create_requesting_ads
from core.models import Advertisement

class TestAllDailyEmailScenarios(common_set_up_classes.SetUpNewsEmailsTesting):

    def setUp(cls):

        cls.offering_ad_no_areas = create_offering_ads(
            province=cls.province,
            municipality=cls.municipality,
            user=cls.user_dict['user_1'],
            is_published=True,
            created_at=cls.one_hour_back,
        )

        cls.offering_ad_with_areas = create_offering_ads(
            province=cls.province,
            municipality=cls.municipality,
            area=cls.area_1,
            user=cls.user_dict['user_1'],
            is_published=True,
            created_at=cls.one_hour_back,
        )

        cls.requesting_ad_no_areas = create_requesting_ads(
            province=cls.province,
            municipality=cls.municipality,
            user=cls.user_dict['user_1'],
            is_published=True,
            created_at=cls.one_hour_back,
        )

        cls.requesting_ad_with_areas = create_requesting_ads(
            province=cls.province,
            municipality=cls.municipality,
            area=cls.area_1,
            user=cls.user_dict['user_1'],
            is_published=True,
            created_at=cls.one_hour_back,
        )

    def test_all_types_of_news_email_objects_get_subscription_mail(self):
        result = call_command('daily_subscribe_mails')

        self.assertIn(str(self.news_email_daily_offering_without_area.pk), result)
        self.assertIn(str(self.news_email_daily_offering_with_area.pk), result)
        self.assertIn(str(self.news_email_daily_requesting_without_area.pk), result)
        self.assertIn(str(self.news_email_daily_offering_with_area.pk), result)


class TestOnlyMailsWithin24HoursGoOut(common_set_up_classes.SetUpNewsEmailsTesting):

    def setUp(cls):
        
        cls.offering_ad_no_areas = create_offering_ads(
            province=cls.province,
            municipality=cls.municipality,
            user=cls.user_dict['user_1'],
            is_published=True,
            created_at=cls.twenty_three_hours_back,
        )


        cls.requesting_ad_no_areas = create_requesting_ads(
            province=cls.province,
            municipality=cls.municipality,
            user=cls.user_dict['user_1'],
            is_published=True,
            created_at=cls.twenty_five_hours_back,
        )



    def test_ad_created_earlier_than_24_hours_ago_dont_generate_mail(self):

        ad = Advertisement.objects.create(author=self.user_dict['user_1'], municipality=self.municipality, province=self.province, created_at=self.twenty_five_hours_back)

        print('custom ad', ad.created_at)
        print('updated at', ad.updated_at)

        ad.updated_at = self.twenty_five_hours_back
        ad.save()
        
        print('updated at', ad.updated_at)



        print('FROM TESTS', self.requesting_ad_no_areas[0].created_at)
        result = call_command('daily_subscribe_mails')

        print(result)
        