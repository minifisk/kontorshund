import pytz 
import datetime

from django.core.management.base import BaseCommand, CommandError
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from core.models import Province, Municipality, Area, Advertisement, NewsEmail

import logging 
logger = logging.getLogger(__name__)



class Command(BaseCommand):
    help = 'Sending remainer 1 week before ad as inactivated'

    def handle(self, *args, **options):

        logger.info('[1_WEEK_BEFORE_AD_INACTIVE_REMINDERS] Starting command for sending reminder emails...')

        utc_sthlm=pytz.timezone('Europe/Stockholm')
        eight_days_ahead_no_tz = datetime.datetime.now() + datetime.timedelta(days=8)
        six_days_ahead_no_tz = datetime.datetime.now() + datetime.timedelta(days=6)

        eight_days_ahead_date = utc_sthlm.localize(eight_days_ahead_no_tz.date()) 
        six_days_ahead_date = utc_sthlm.localize(six_days_ahead_no_tz.date()) 


        # Get all ads where deletion_date is between 6 and 8 (i.e. 7 days) ahead from today


        # Send email to all authors

        # swish-pay/extend/<int:pk>







        ad_root_path = 'https://www.kontorshund.se/ads/'
        number_of_mails_sent = 0

        logger.info('[WEEKLY_SUBSCRIBE_EMAILS] Sending emails to subscribers matching "offering" ads...')

        # OFFERING

        all_weekly_offering_subscriptions = NewsEmail.get_all_active_weekly_subscriptions('offering')
        all_active_offering_ads = Advertisement.get_all_active_offering_ads()

        for news_email_subscription_object in all_weekly_offering_subscriptions:
            if news_email_subscription_object.areas:

                area_list = []
                area_list_names = []

                for area in news_email_subscription_object.areas.all():
                    area_list.append(area)
                    area_list_names.append(area.name)

                matching_ads = all_active_offering_ads.filter(
                    created_at__gte=one_week_back, 
                    province=news_email_subscription_object.province,
                    municipality=news_email_subscription_object.municipality,
                    area__in=area_list
                )

                matching_ads_count = matching_ads.count()

                if matching_ads:

                    context = {
                        'ads': matching_ads,
                        'ad_root_path': ad_root_path,
                        'subscribed_province': news_email_subscription_object.province,
                        'subscribed_municipality': news_email_subscription_object.municipality,
                        'subscribed_area': area_list,
                        'ad_type': news_email_subscription_object.ad_type,
                        'news_email_uuid': news_email_subscription_object.uuid,
                        'ad_count': matching_ads_count,
                        'interval': 'weekly',
                        'subscription_uuid': news_email_subscription_object.uuid,
                    }

                    subject = f'{matching_ads_count} nya annonser på Kontorshund.se!'
                    html_message = render_to_string('core/subscription_email/daily_mail.html', {**context})
                    plain_message = strip_tags(html_message)
                    from_email = 'Kontorshund.se <info@kontorshund.se>'
                    to = news_email_subscription_object.user.email

                    send_mail(subject, plain_message, from_email, [to], html_message=html_message)
                    number_of_mails_sent += 1

            else: 

                all_active_offering_ads.filter(
                    created_at__gte=one_week_back, 
                    province=news_email_subscription_object.province,
                    municipality=news_email_subscription_object.municipality,
                )

                matching_ads_count = matching_ads.count()

                if matching_ads:

                    context = {
                        'ads': matching_ads,
                        'ad_root_path': ad_root_path,
                        'subscribed_province': news_email_subscription_object.province,
                        'subscribed_municipality': news_email_subscription_object.municipality,
                        'ad_type': news_email_subscription_object.ad_type,
                        'news_email_uuid': news_email_subscription_object.uuid,
                        'count_ads': matching_ads_count,
                        'interval': 'weekly',
                        'subscription_uuid': news_email_subscription_object.uuid,
                    }

                    subject = f'{matching_ads_count} nya annonser på Kontorshund.se!'
                    html_message = render_to_string('core/subscription_email/daily_mail.html', {'context': context})
                    plain_message = strip_tags(html_message)
                    from_email = 'Kontorshund.se <info@kontorshund.se>'
                    to = news_email_subscription_object.user.email

                    send_mail(subject, plain_message, from_email, [to], html_message=html_message)
                    number_of_mails_sent += 1


        offering_emails_sent = number_of_mails_sent
        logger.info(f'[WEEKLY_SUBSCRIBE_EMAILS] Finished sending mails for "offering"-ads, sent {offering_emails_sent} emails')

        
        # REQUESTING

        logger.info('[WEEKLY_SUBSCRIBE_EMAILS] Sending emails to subscribers matching "requesting" ads...')

        all_weekly_requesting_subscriptions = NewsEmail.get_all_active_weekly_subscriptions('requesting')
        all_active_requesting_ads = Advertisement.get_all_active_requesting_ads()

        for news_email_subscription_object in all_weekly_requesting_subscriptions:

            if news_email_subscription_object.areas:

                area_list = []
                area_list_names = []
                for area in news_email_subscription_object.areas.all():
                    area_list.append(area)
                    area_list_names.append(area.name)

                matching_ads = all_active_requesting_ads.filter(
                    created_at__gte=one_week_back, 
                    province=news_email_subscription_object.province,
                    municipality=news_email_subscription_object.municipality,
                    area__in=area_list
                )

                matching_ads_count = matching_ads.count()

                if matching_ads:

                    context = {
                        'ads': matching_ads,
                        'ad_root_path': ad_root_path,
                        'subscribed_province': news_email_subscription_object.province,
                        'subscribed_municipality': news_email_subscription_object.municipality,
                        'subscribed_area': area_list_names,
                        'ad_type': news_email_subscription_object.ad_type,
                        'news_email_uuid': news_email_subscription_object.uuid,
                        'ad_count': matching_ads_count,
                        'interval': 'weekly',
                        'subscription_uuid': news_email_subscription_object.uuid,
                    }

                    subject = f'{matching_ads_count} nya annonser på Kontorshund.se!'
                    html_message = render_to_string('core/subscription_email/daily_mail.html', {**context})
                    plain_message = strip_tags(html_message)
                    from_email = 'Kontorshund.se <info@kontorshund.se>'
                    to = news_email_subscription_object.user.email

                    send_mail(subject, plain_message, from_email, [to], html_message=html_message)
                    number_of_mails_sent += 1

            else: 

                all_active_requesting_ads.filter(
                    created_at__gte=one_week_back, 
                    province=news_email_subscription_object.province,
                    municipality=news_email_subscription_object.municipality,
                )

                matching_ads_count = matching_ads.count()

                if matching_ads:

                    context = {
                        'ads': matching_ads,
                        'ad_root_path': ad_root_path,
                        'subscribed_province': news_email_subscription_object.province,
                        'subscribed_municipality': news_email_subscription_object.municipality,
                        'ad_type': news_email_subscription_object.ad_type,
                        'news_email_uuid': news_email_subscription_object.uuid,
                        'count_ads': matching_ads_count,
                        'interval': 'weekly',
                        'subscription_uuid': news_email_subscription_object.uuid,
                    }

                    subject = f'{matching_ads_count} nya annonser på Kontorshund.se!'
                    html_message = render_to_string('core/subscription_email/daily_mail.html', {'context': context})
                    plain_message = strip_tags(html_message)
                    from_email = 'Kontorshund.se <info@kontorshund.se>'
                    to = news_email_subscription_object.user.email

                    send_mail(subject, plain_message, from_email, [to], html_message=html_message)
                    number_of_mails_sent += 1
        
        
        requesting_emails_sent = number_of_mails_sent - offering_emails_sent
        logger.info(f'[WEEKLY_SUBSCRIBE_EMAILS] Finished sending mails for "requesting"-ads, sent {requesting_emails_sent} emails')


        logger.info(f'[WEEKLY_SUBSCRIBE_EMAILS] FINISHED COMMAND - Sent a total of {number_of_mails_sent} emails to customers!')