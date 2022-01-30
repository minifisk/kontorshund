import datetime

from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from kontorshund.settings import PRICE_SWISH_EXTEND

from core.models import Advertisement

import logging 
logger = logging.getLogger(__name__)



class Command(BaseCommand):
    help = 'Inactivating ads who run out on current date, and send emails for extending ad option'

    def handle(self, *args, **options):

        current_date_datetime = datetime.datetime.now() 
        current_date = current_date_datetime.date()

        logger.info(f'[DEACTIVATE_ADS_ON_DELETION_DATE] Starting command for deactivating ads whos deletion date on the date {current_date}')


        number_of_mails_sent = 0

        all_ads = Advertisement.get_all_active_ads()

        ad_selection = all_ads.filter(deletion_date=current_date)


        if ad_selection:

            for ad in ad_selection:

                ad.is_active = False
                ad.is_deleted = True
                ad.save()

                context = {
                    'ad': ad,
                    'renewal_price': PRICE_SWISH_EXTEND
                }


                subject = 'Din annons på Kontorshund.se har gått ut.'
                html_message = render_to_string('core/renewal_email/ad_was_set_inactive.html', context)
                plain_message = strip_tags(html_message)
                from_email = 'Kontorshund.se <info@kontorshund.se>'
                to = ad.author.email

                send_mail(subject, plain_message, from_email, [to], html_message=html_message)
                
                number_of_mails_sent += 1



        logger.info(f'[DEACTIVATE_ADS_ON_DELETION_DATE] Sent out a number of {number_of_mails_sent} emails and inactivated associated ads.')