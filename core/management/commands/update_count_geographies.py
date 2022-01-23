from django.core.management.base import BaseCommand, CommandError
from core.models import Province, Municipality, Area,Advertisement

class Command(BaseCommand):
    help = 'Updating offering & requesting count on Province, Municipality and Area'

    def handle(self, *args, **options):

        # Get all active ads
        all_active_ads = Advertisement.get_all_active_ads()

        # Update count for province's
        all_province_obj = Province.objects.all()

        for province in all_province_obj:
            offering_count_ads_in_province = all_active_ads.filter(province=province, is_offering_own_dog=True).count()
            requesting_count_ads_in_province = all_active_ads.filter(province=province, is_offering_own_dog=False).count()

            province.offering_count = offering_count_ads_in_province
            province.requesting_count = requesting_count_ads_in_province
            province.save()

        all_municipality_obj = Municipality.objects.all()

        # Update count for municipalities's
        for municipality in all_municipality_obj:
            offering_count_ads_in_municipality = all_active_ads.filter(municipality=municipality, is_offering_own_dog=True).count()
            requesting_count_ads_in_municipality = all_active_ads.filter(municipality=municipality, is_offering_own_dog=False).count()

            municipality.offering_count = offering_count_ads_in_municipality
            municipality.requesting_count = requesting_count_ads_in_municipality
            municipality.save()

        all_area_obj = Area.objects.all()

        # Update count for areas's
        for area in all_area_obj:
            offering_count_ads_in_area = all_active_ads.filter(area=area, is_offering_own_dog=True).count()
            requesting_count_ads_in_area = all_active_ads.filter(area=area, is_offering_own_dog=False).count()

            area.offering_count = offering_count_ads_in_area
            area.requesting_count = requesting_count_ads_in_area
            area.save()
