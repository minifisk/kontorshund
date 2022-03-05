from core.tests import common_set_up_classes
from django.core.management import call_command

from core.tests.factories import create_offering_ads, create_requesting_ads
from core.models import Advertisement

class TestAllWeeklyEmailScenarios(common_set_up_classes.SetUpNewsEmailsTesting):

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
        result = call_command('weekly_subscribe_mails')

        self.assertIn(str(self.news_email_weekly_offering_without_area.pk), result)
        self.assertIn(str(self.news_email_weekly_offering_with_area.pk), result)
        self.assertIn(str(self.news_email_weekly_requesting_without_area.pk), result)
        self.assertIn(str(self.news_email_weekly_offering_with_area.pk), result)


class TestOnlyMailsWithinOneWeekGoOut(common_set_up_classes.SetUpNewsEmailsTesting):

    def setUp(cls):
        
        cls.offering_ad_no_areas = create_offering_ads(
            province=cls.province,
            municipality=cls.municipality,
            user=cls.user_dict['user_1'],
            is_published=True,
            created_at=cls.six_days_ago,
        )


        cls.requesting_ad_no_areas = create_requesting_ads(
            province=cls.province,
            municipality=cls.municipality,
            user=cls.user_dict['user_1'],
            is_published=True,
            created_at=cls.eight_days_ago,
        )



    def test_ad_created_earlier_than_one_week_ago_dont_generate_mail(self):

        result = call_command('weekly_subscribe_mails')

        self.assertIn(str(self.news_email_weekly_offering_without_area.pk), result)
        self.assertNotIn(str(self.news_email_weekly_requesting_without_area.pk), result)
        