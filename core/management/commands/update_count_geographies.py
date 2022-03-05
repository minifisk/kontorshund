from django.core.management.base import BaseCommand
from core.models import Province, Municipality, Area,Advertisement
from core.models import AdKind

class Command(BaseCommand):
    help = 'Updating offering & requesting count on Province, Municipality and Area'

    def handle(self, *args, **options):

        all_active_ads = Advertisement.get_all_active_ads()
        ad_kind_requesting = AdKind.REQUESTING
        ad_kind_offering = AdKind.OFFERING

        # Update count for province's
        all_province_obj = Province.objects.all()

        for province in all_province_obj:
            offering_ads_count_in_province = all_active_ads.filter(province=province, ad_kind=ad_kind_offering).count()
            requesting_ads_count_in_province = all_active_ads.filter(province=province, ad_kind=ad_kind_requesting).count()

            province.offering_count = offering_ads_count_in_province
            province.requesting_count = requesting_ads_count_in_province
            province.save()

        all_municipality_obj = Municipality.objects.all()

        # Update count for municipalities's
        for municipality in all_municipality_obj:
            offering_ads_count_in_municipality = all_active_ads.filter(municipality=municipality,  ad_kind=ad_kind_offering).count()
            requesting_ads_count_in_municipality = all_active_ads.filter(municipality=municipality, ad_kind=ad_kind_requesting).count()

            municipality.offering_count = offering_ads_count_in_municipality
            municipality.requesting_count = requesting_ads_count_in_municipality
            municipality.save()

        all_area_obj = Area.objects.all()

        # Update count for areas's
        for area in all_area_obj:
            offering_ads_count_in_area = all_active_ads.filter(area=area, ad_kind=ad_kind_offering).count()
            requesting_ads_count_in_area = all_active_ads.filter(area=area, ad_kind=ad_kind_requesting).count()

            area.offering_count = offering_ads_count_in_area
            area.requesting_count = requesting_ads_count_in_area
            area.save()
