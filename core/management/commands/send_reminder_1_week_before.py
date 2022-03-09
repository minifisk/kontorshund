import json
import pytz 
import datetime

from django.core.management.base import BaseCommand, CommandError
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from common.prices import CURRENT_PRICE_STRING

from core.models import Province, Municipality, Area, Advertisement, NewsEmail

import logging 
logger = logging.getLogger(__name__)



class Command(BaseCommand):
    help = 'Sending remainer 1 week before ad as inactivated'

    def handle(self, *args, **options):

        logger.info('[1_WEEK_BEFORE_AD_INACTIVE_REMINDERS] Starting command for sending reminder emails...')


        today = datetime.datetime.now(pytz.timezone('Europe/Stockholm')).date()
        seven_days_ahead_date = today + datetime.timedelta(days=7)

        number_of_mails_sent = 0
        sent_mail_to_ads_with_pk = []

        all_ads = Advertisement.get_all_active_ads()

        for ad in all_ads:
            print(ad.deletion_date)

        # Get all ads where deletion_date is between 6 and 8 (i.e. 7 days) ahead from today

        ad_selection = all_ads.filter(deletion_date=seven_days_ahead_date)

        if ad_selection:

            for ad in ad_selection:

                context = {
                    'ad': ad,
                    'renewal_price': CURRENT_PRICE_STRING
                }

                subject = 'Din annons på Kontorshund.se går ut om en vecka!'
                html_message = render_to_string('core/renewal_email/one_week_left.html', context)
                plain_message = strip_tags(html_message)
                from_email = 'Kontorshund.se <info@kontorshund.se>'
                to = ad.author.email

                sent_mail_to_ads_with_pk.append(ad.pk)
                send_mail(subject, plain_message, from_email, [to], html_message=html_message)
                
                number_of_mails_sent += 1


        logger.info(f'[1_WEEK_BEFORE_AD_INACTIVE_REMINDERS] Sent out reminders to ads with pks {sent_mail_to_ads_with_pk}')
        logger.info(f'[1_WEEK_BEFORE_AD_INACTIVE_REMINDERS] Sent out a number of {number_of_mails_sent} reminder emails to customers.')

        sent_mail_to_ads_with_pk_json = json.dumps(sent_mail_to_ads_with_pk)

        return sent_mail_to_ads_with_pk_json