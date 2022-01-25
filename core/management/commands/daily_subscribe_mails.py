from django.core.management.base import BaseCommand, CommandError
from core.models import Province, Municipality, Area, Advertisement, NewsEmail
import datetime
from django.core.mail import send_mail

from django.template.loader import render_to_string
from django.utils.html import strip_tags


import logging 
logger = logging.getLogger(__name__)



class Command(BaseCommand):
    help = 'Updating offering & requesting count on Province, Municipality and Area'

    def handle(self, *args, **options):

        logger.info('Starting command for sending daily emails...')

        # Get all _active_ newsemail objects with a _daily_ subscription
        all_daily_offering_subscriptions = NewsEmail.get_all_active_daily_subscriptions('offering')
        all_daily_requesting_subscriptions = NewsEmail.get_all_active_daily_subscriptions('requesting')

        date_from = datetime.datetime.now() - datetime.timedelta(days=1)

        ad_root_path = 'https://www.kontorshund.se/ads/'

        number_of_mails_sent = 0

        # OFFERING
        all_active_offering_ads = Advertisement.get_all_active_offering_ads()

        # Iterate over each newsemail object
        for news_email_subscription_object in all_daily_offering_subscriptions:

            # If area provided in subscription
            if news_email_subscription_object.areas:

                area_list = []
                for area in news_email_subscription_object.areas.all():
                    area_list.append(area)

                # Gather all ads matching Province/Municipality/Area & ad_type that's been created during last 24 hours
                matching_ads = all_active_offering_ads.filter(
                    created_at__gte=date_from, 
                    province=news_email_subscription_object.province,
                    municipality=news_email_subscription_object.municipality,
                    area__in=area_list
                )



                matching_ads_count = matching_ads.count()

                # If any ads found, send email
                if matching_ads:

                    context = {
                        'ads': matching_ads,
                        'ad_root_path': ad_root_path,
                        'subscribed_province': news_email_subscription_object.province,
                        'subscribed_municipality': news_email_subscription_object.municipality,
                        'subscribed_area': news_email_subscription_object.areas,
                        'ad_type': news_email_subscription_object.ad_type,
                        'news_email_uuid': news_email_subscription_object.uuid,
                        'ad_count': matching_ads_count
                    }

                    subject = f'{matching_ads_count} nya annonser på Kontorshund.se!'
                    html_message = render_to_string('core/subscription_email/daily_mail.html', {**context})
                    plain_message = strip_tags(html_message)
                    from_email = 'info@kontorshund.se'
                    to = news_email_subscription_object.user.email

                    send_mail(subject, plain_message, from_email, [to], html_message=html_message)
                    number_of_mails_sent += 1

            else: 
                # If area hasn't been provided in subscription

                # Gather all ads matching Province/Municipality & ad_type that has been created during the last 24 hours
                all_active_offering_ads.filter(
                    created_at__gte=date_from, 
                    province=news_email_subscription_object.province,
                    municipality=news_email_subscription_object.municipality,
                )

                matching_ads_count = matching_ads.count()

                # If any ads found, send email
                if matching_ads:

                    context = {
                        'ads': matching_ads,
                        'ad_root_path': ad_root_path,
                        'subscribed_province': news_email_subscription_object.province,
                        'subscribed_municipality': news_email_subscription_object.municipality,
                        'ad_type': news_email_subscription_object.ad_type,
                        'news_email_uuid': news_email_subscription_object.uuid,
                        'count_ads': matching_ads_count
                    }

                    subject = f'{matching_ads_count} nya annonser på Kontorshund.se!'
                    html_message = render_to_string('core/subscription_email/daily_mail.html', {'context': context})
                    plain_message = strip_tags(html_message)
                    from_email = 'From <info@kontorshund.se'
                    to = news_email_subscription_object.user.email

                    send_mail(subject, plain_message, from_email, [to], html_message=html_message)
                    number_of_mails_sent += 1


        
        logger.info(f'Finished command for sending daily mails, Sent a total of {number_of_mails_sent} emails to customers!')