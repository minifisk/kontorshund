import pytz 
import datetime

from django.core.management.base import BaseCommand, CommandError
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from kontorshund.settings import PRICE_SWISH_EXTEND

from core.models import Province, Municipality, Area, Advertisement, NewsEmail

import logging 
logger = logging.getLogger(__name__)



class Command(BaseCommand):
    help = 'Sending remainer 1 week before ad as inactivated'

    def handle(self, *args, **options):

        logger.info('[1_WEEK_BEFORE_AD_INACTIVE_REMINDERS] Starting command for sending reminder emails...')

        seven_days_ahead_datetime = datetime.datetime.now() + datetime.timedelta(days=7)
        seven_days_ahead_date = seven_days_ahead_datetime.date()

        number_of_mails_sent = 0

        all_ads = Advertisement.get_all_active_ads()

        # Get all ads where deletion_date is between 6 and 8 (i.e. 7 days) ahead from today

        ad_selection = all_ads.filter(deletion_date=seven_days_ahead_date)

        if ad_selection:

            for ad in ad_selection:

                context = {
                    'ad': ad,
                    'renewal_price': PRICE_SWISH_EXTEND
                }


                subject = 'Din annons på Kontorshund.se går ut om en vecka!'
                html_message = render_to_string('core/renewal_email/one_week_left.html', context)
                plain_message = strip_tags(html_message)
                from_email = 'Kontorshund.se <info@kontorshund.se>'
                to = ad.author.email

                send_mail(subject, plain_message, from_email, [to], html_message=html_message)
                
                number_of_mails_sent += 1



        logger.info(f'[1_WEEK_BEFORE_AD_INACTIVE_REMINDERS] Sent out a number of {number_of_mails_sent} reminder emails to customers.')

