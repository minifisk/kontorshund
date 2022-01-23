from django.core.management.base import BaseCommand, CommandError
from core.models import Province, Municipality, Area, Advertisement, NewsEmail
import datetime

class Command(BaseCommand):
    help = 'Updating offering & requesting count on Province, Municipality and Area'

    def handle(self, *args, **options):

        pass
        # Get all _active_ newsemail objects with a _daily_ subscription
        all_daily_offering_subscriptions = NewsEmail.get_all_active_daily_subscriptions('offering')
        all_daily_requesting_subscriptions = NewsEmail.get_all_active_daily_subscriptions('requesting')

        date_from = datetime.datetime.now() - datetime.timedelta(days=1)

        # OFFERING
            
        # Iterate over each newsemail object
        for subscription in all_daily_offering_subscriptions:

            # If area provided
            if subscription.area:

                # Gather all ads matching Province/Municipality/Area & ad_type that's been created during last 24 hours
                all_ads = Advertisement.get_all_active_offering_ads.filter(created_at__gte=date_from)

                # If any ads found, send email
                if all_ads:
                    pass

                # If area hasn't been provided

                    # Gather all ads matching Province/Municipality & ad_type that has been created during the last 24 hours
