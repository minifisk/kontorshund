import datetime
import json
import pytz

from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from common.prices import CURRENT_PRICE_STRING

from core.models import Advertisement

import logging 
logger = logging.getLogger(__name__)



class Command(BaseCommand):
    help = 'Inactivating ads who run out on current date, and send emails for extending ad option'

    def handle(self, *args, **options):

        current_date = datetime.datetime.now(pytz.timezone('Europe/Stockholm')).date()
        deactivated_ads_pks = []

        logger.info(f'[DEACTIVATE_ADS_ON_DELETION_DATE] Starting command for deactivating ads whos deletion date on the date {current_date}')

        number_of_mails_sent = 0

        all_ads = Advertisement.get_all_active_ads()

        ad_selection = all_ads.filter(deletion_date__lte=current_date)


        if ad_selection:

            for ad in ad_selection:

                ad.is_active = False
                ad.is_deleted = True
                ad.save()

                context = {
                    'ad': ad,
                    'renewal_price': CURRENT_PRICE_STRING
                }


                subject = 'Din annons på Kontorshund.se har gått ut.'
                html_message = render_to_string('core/renewal_email/ad_was_set_inactive.html', context)
                plain_message = strip_tags(html_message)
                from_email = 'Kontorshund.se <info@kontorshund.se>'
                to = ad.author.email

                deactivated_ads_pks.append(ad.pk)
                send_mail(subject, plain_message, from_email, [to], html_message=html_message)
                
                number_of_mails_sent += 1


        logger.info(f'[DEACTIVATE_ADS_ON_DELETION_DATE] Deactivated the following ads: {deactivated_ads_pks}')

        logger.info(f'[DEACTIVATE_ADS_ON_DELETION_DATE] Sent out a number of {number_of_mails_sent} emails and inactivated associated ads.')

        deactivated_ads_pks_json = json.dumps(deactivated_ads_pks)

        return(deactivated_ads_pks_json)