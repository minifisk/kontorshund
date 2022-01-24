from django.core.management.base import BaseCommand, CommandError
from core.models import Province, Municipality, Area, Advertisement, NewsEmail
import datetime
from django.core.mail import send_mail

from django.template.loader import render_to_string
from django.utils.html import strip_tags




class Command(BaseCommand):
    help = 'Updating offering & requesting count on Province, Municipality and Area'

    def handle(self, *args, **options):


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
                    send_mail(
                        subject='Hejsan',
                        message='Tjenare igen',
                        from_email='info@kontorshund.se',
                        recipient_list=['alexlindgren08@gmail.com'],
                    )
                    
                    pass

                    subject = 'Subject'
                    html_message = render_to_string('mail_template.html', {'context': 'values'})
                    plain_message = strip_tags(html_message)
                    from_email = 'From <from@example.com>'
                    to = 'to@example.com'

mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)


                # If area hasn't been provided

                    # Gather all ads matching Province/Municipality & ad_type that has been created during the last 24 hours
