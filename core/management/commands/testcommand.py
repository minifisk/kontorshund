
import datetime
from core.models import Advertisement
import pytz


from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Sending weekly subscribe emails'

    def handle(self, *args, **options):

        utc_sthlm=pytz.timezone('Europe/Stockholm')

        all_ads = Advertisement.objects.all()

        one_week_back = datetime.datetime.now() - datetime.timedelta(days=7)
        one_week_back = utc_sthlm.localize(one_week_back) 

        for ad in all_ads:
            print(ad.pk)
            #print(ad.created_at)
            local_create_at = ad.created_at.replace(tzinfo=pytz.utc).astimezone(utc_sthlm)
            print(local_create_at)
            print(one_week_back)
            print(ad.created_at >= one_week_back)
