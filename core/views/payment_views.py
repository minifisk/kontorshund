import datetime
import io
from django import http
from django.views import View
import qrcode 
import json
import requests
import json
import locale
from urllib.parse import urljoin
from pprint import pprint 

from django.http.response import HttpResponseNotFound, HttpResponseRedirect, JsonResponse
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models import F
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from core.models import PaymentKind

from kontorshund.settings import SWISH_PAYEEALIAS, SWISH_URL, SWISH_CERT, SWISH_ROOTCA, NGROK_URL

from common.prices import get_current_ad_price_as_int_and_string
from core.models import Advertisement, get_one_month_ahead_from_date_obj, get_one_month_ahead_from_today

User = get_user_model()

locale.setlocale(locale.LC_ALL,'sv_SE.UTF-8')

import logging 
logger = logging.getLogger(__name__)


#################
# PAYMENT STATUS
#################

class CheckInitialPaymentStatus(View):
    """ 
    Support function for checking an initial payment status for an ad.
    """

    def post(self, request, pk):
        if request.user.is_authenticated:
            try:
                ad = Advertisement.objects.get(pk=pk)
            except Advertisement.DoesNotExist:
                logger.exception(f'User {request.user.pk} checked extended payment status for ad {pk}, which returned an doesnotexist error')
                return JsonResponse("Ad does not exist", status=404, safe=False)
            if request.user == ad.author:
                logger.debug(f'User {request.user.pk} checked initial payment status for ad {pk}')
                try:
                    ad = Advertisement.objects.get(pk=pk)
                except Advertisement.DoesNotExist:
                    logger.exception(f'User {request.user.pk} checked initial payment status for ad {pk}, which returned an doesnotexist error')
                    return JsonResponse("Ad does not exist", status=404, safe=False)

                if ad.has_initial_payment:
                    logger.debug(f'User {request.user.pk} checking initial payment status for ad {pk}, which returned True')
                    return JsonResponse("Payment is complete!", status=200, safe=False)
                else:
                    logger.debug(f'User {request.user.pk} checking initial payment status for ad {pk}, which returned False')
                    return JsonResponse("Payment is NOT complete", status=404, safe=False)
            else:
                logger.debug(f'User {request.user.pk} tried checking initial payment status for ad ({pk}) belonging to another user, redirecting to profile...')
                return redirect('profile')

        else:
            return redirect('account_login')

    

class CheckExtendedPaymentStatus(View):
    """ 
    Support function for checking an extended payment status for an ad.
    """

    def post(self, request, pk):
        if request.user.is_authenticated:
            try:
                ad = Advertisement.objects.get(pk=pk)
            except Advertisement.DoesNotExist:
                logger.exception(f'User {request.user.pk} checked extended payment status for ad {pk}, which returned an doesnotexist error')
                return JsonResponse("Ad does not exist", status=404, safe=False)
            if request.user == ad.author:
                logger.debug(f'User {request.user.pk} checked extended payment status for ad {pk}')

                if ad.has_extended_payment:
                    logger.debug(f'User {request.user.pk} checking initial payment status for ad {pk}, which returned True')
                    return JsonResponse("Payment is complete!", status=200, safe=False)
                else:
                    logger.debug(f'User {request.user.pk} checking initial payment status for ad {pk}, which returned False')
                    return JsonResponse("Payment is NOT complete", status=404, safe=False)
            else:
                logger.debug(f'User {request.user.pk} tried checking initial payment status for ad ({pk}) belonging to another user, redirecting to profile...')
                return redirect('profile')
        else:
            return redirect('account_login')


###################
# ANDROID SPECIFIC
###################

class AndroidSuccessPage(View):

    def get(self, request):
        logger.debug('Android success-page was requested and served')
        return render(request, 'core/payment/android_swish_success.html')

#############
# SWISH VIEWS
#############

class SwishCallback(View):
    """ 
    Callback view which recieves a POST request from Swish when a payment have been recieved.
    """

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(SwishCallback, self).dispatch(request, *args, **kwargs)

    def post(self, request):

        data=request.body
        data_dict = json.loads(data.decode("utf-8"))

        # Check if payment was successfull
        if data_dict['status'] == 'PAID':
            logger.debug('Swish callback view was called')

            ad_id = data_dict['payeePaymentReference']
            amount = data_dict['amount']
            date_paid_str = data_dict['datePaid']
            date_paid_obj = datetime.datetime.strptime(date_paid_str, '%Y-%m-%dT%H:%M:%S.%f%z')
            payment_reference = data_dict['paymentReference']
            payer_alias = data_dict['payerAlias']

            logger.debug(
                f'Swish callback view was called, ad id {ad_id} amount {amount} payment_reference {payment_reference} payer alias {payer_alias}'
            )
            try:
                ad_obj = Advertisement.objects.get(pk=ad_id) 
            except Advertisement.DoesNotExist:
                logger.exception(f'Ad could not be found in Swish callback view, ad id {ad_id} amount {amount} payment_reference {payment_reference} payer alias {payer_alias}')
                return JsonResponse("Annonsen hittades ej", status=404, safe=False)

            # If payment is extended
            if ad_obj.has_initial_payment:

                payment_obj = ad_obj.create_payment(
                    payment_kind=PaymentKind.EXTENDED, 
                    amount=amount, 
                    payment_reference=payment_reference,
                    date_time_paid = date_paid_obj,
                    payer_alias = payer_alias
                    )

                logger.info(
                    f'Initial payment found - creating extended payment pk {payment_obj.pk}for when Swish callback view was requested, ad id {ad_obj.pk} amount {amount} payment_reference {payment_reference} payer alias {payer_alias}'
                )

                ad_obj.is_published = True
                ad_obj.is_deleted = False


                # Base case - add 30 day ahead from today 
                new_deletion_date = get_one_month_ahead_from_today()

                # If deletion date is later than today, add 30 days ontop of that
                if get_one_month_ahead_from_date_obj(ad_obj.deletion_date) > new_deletion_date:
                    new_deletion_date = get_one_month_ahead_from_date_obj(ad_obj.deletion_date)

                logger.debug(
                    f'Setting deletion date for ad {ad_obj.pk} to {new_deletion_date} for when Swish callback view was requested, ad id {ad_obj.pk} amount {amount} payment_reference {payment_reference} payer alias {payer_alias}'
                )

                ad_obj.deletion_date = new_deletion_date
                ad_obj.save()

                return HttpResponse(status=200)

            # If payment is initial
            else:

                payment_obj = ad_obj.create_payment(
                    payment_kind=PaymentKind.INITIAL, 
                    amount=amount, 
                    payment_reference=payment_reference,
                    date_time_paid = date_paid_obj,
                    payer_alias = payer_alias
                    )

                ad_obj.is_published = True      
                ad_obj.is_deleted = False      
                ad_obj.save()

                logger.info(
                    f'Initial payment not found - creating initial payment pk {payment_obj.pk} for when Swish callback view was requested, ad id {ad_obj.pk} amount {amount} payment_reference {payment_reference} payer alias {payer_alias}'
                )
                return HttpResponse(status=200)

        else:
            error_code = data_dict['errorCode']
            error_message = data_dict['errorCode']

            if error_code != "TM01":
                logger.error(f'Problem creating payment: {error_code} {error_message}')
                return HttpResponse(status=200)
            
            return HttpResponse(status=200)


# For mobile payments
class GenerateSwishPaymentRequestToken(View):
    """ 
    Generate a PaymentRequestToken, used for users visiting from Mobile where they have the Swish application
    installed, when token have been generated, the Swish app opens at the users phone.
    """

    def post(self, request, pk):

        if request.user.is_authenticated:

            CURRENT_PRICE, CURRENT_PRICE_STRING = get_current_ad_price_as_int_and_string()

            PRICE_TO_PAY = CURRENT_PRICE

            try: 
                ad_obj = Advertisement.objects.get(pk=pk)
            except Advertisement.DoesNotExist():
                logger.exception(f'Failed to find Advertisement with pk {pk} when User with pk {request.user.pk} was requesting swish Payment request token ')
                return HttpResponseNotFound("Annonsen kunde inte hittas")  

            if ad_obj.has_initial_payment:
                PRICE_TO_PAY = CURRENT_PRICE
                    
            ##########################
            # Enable for local testing
            #SWISH_CALLBACKURL = urljoin(NGROK_URL, "/swish/callback")
            ##########################
        
            url = request.build_absolute_uri('/')
            callback_path = f'swish/callback'

            ##################
            # Enable for prod
            SWISH_CALLBACKURL= f'{url}{callback_path}'
            ##################

            # Set-up variables for payment request
            payload = {
                "payeePaymentReference": pk,
                "callbackUrl": SWISH_CALLBACKURL,
                "payeeAlias": SWISH_PAYEEALIAS,
                "currency": "SEK",
                "amount": PRICE_TO_PAY,
                "message": f"Betalning för annons med ID {pk}"
            }

            resp = requests.post(urljoin(SWISH_URL, "v1/paymentrequests"), json=payload, cert=SWISH_CERT, verify=SWISH_ROOTCA, timeout=2)
            PaymentRequestToken = resp.headers['PaymentRequestToken']
            logger.info(f'Returning swish-payment-request-token to User with pk {request.user.pk}, for ad with pk {pk} for amount {PRICE_TO_PAY}')
            return JsonResponse({'token': PaymentRequestToken, 'callback_url': SWISH_CALLBACKURL}, status=201, safe=False)
        else:
            return redirect('account_login')


# Support function for below View
def get_qr_code(request, token):
    if request.user.is_authenticated:
        qr = qrcode.QRCode(
            version = 1,
            error_correction = qrcode.constants.ERROR_CORRECT_L,
            box_size = 5,
            border = 0,
        )

        qr.add_data("D" + token)
        qr.make(fit=True)
        qr_img = qr.make_image()

        bytesio_object = io.BytesIO()
        qr_img.save(bytesio_object)

        file_data = bytesio_object.getvalue()
        response = HttpResponse(content_type=f'image/png')
        response['Content-Disposition'] = f'inline; filename="qr-code-image"'
        response.write(file_data)
        return response 
    else:
        return redirect('account_login')


class GenerateSwishPaymentQrCode(View):
    """ 
    Generate a QR code, for users visiting via a desktop computer for either providing initial or extended payment 
    for a users ad.
    """

    def post(self, request, pk):

        if request.user.is_authenticated:
            CURRENT_PRICE, CURRENT_PRICE_STRING = get_current_ad_price_as_int_and_string()

            # Handle price depending on if it's an initial/extened payment
            PRICE_TO_PAY = CURRENT_PRICE

            try: 
                ad_obj = Advertisement.objects.get(pk=pk)
            except Advertisement.DoesNotExist():
                logger.exception(f'Failed to find advertisement when user with pk {request.user.pk} requested payment QR code for ad with pk {pk}')
                return HttpResponseNotFound("Annonsen kunde inte hittas")  

            if ad_obj.has_initial_payment:
                PRICE_TO_PAY = CURRENT_PRICE
            else:
                PRICE_TO_PAY = CURRENT_PRICE

            ##########################
            # Enable for local testing
            #SWISH_CALLBACKURL = urljoin(NGROK_URL, "/swish/callback")
            ##########################

            url = request.build_absolute_uri('/')
            callback_path = f'swish/callback'

            ##################
            # Enable for prod
            SWISH_CALLBACKURL= f'{url}{callback_path}'
            ###################

            # Set-up variables for payment request
            payload = {
                "payeePaymentReference": pk,
                "callbackUrl": SWISH_CALLBACKURL,
                "payeeAlias": SWISH_PAYEEALIAS,
                "currency": "SEK",
                "amount": PRICE_TO_PAY,
                "message": f"Betalning för annons med ID {pk}"
            }

            resp = requests.post(urljoin(SWISH_URL, "v1/paymentrequests"), json=payload, cert=SWISH_CERT, verify=SWISH_ROOTCA, timeout=2)
            PaymentRequestToken = resp.headers['PaymentRequestToken']

            qr_image_response = get_qr_code(request, PaymentRequestToken)
            logger.info(f'Returning swish-payment-QR-code to user with pk {request.user.pk}, for ad with pk {pk} for amount {PRICE_TO_PAY}')
            return qr_image_response
        else:
            return redirect('account_login')


###################
# PAYMENT TEMPLATES
###################

class PayForAdSwishTemplate(View):
    """ 
    Generate template for user for either providing intial or extened payment for their ad.
    """

    def get(self, request, pk):
        if request.user.is_authenticated:

            url = request.build_absolute_uri()
            CURRENT_PRICE, CURRENT_PRICE_STRING = get_current_ad_price_as_int_and_string()

            if 'swish-pay/initial' in url:
            
                try: 
                    ad_obj = Advertisement.objects.get(pk=pk)
                except Advertisement.DoesNotExist():
                    logger.exception(f'Failed to return Advertisement which couldnt be found when user with PK {request.user-pk} requested initial swish payment template')
                    return HttpResponseNotFound("Annonsen kunde inte hittas")     

                if ad_obj.has_initial_payment:
                    return HttpResponseRedirect(reverse_lazy('ad_detail', kwargs={'pk': pk}))

                ad_title = ad_obj.title

                url = request.build_absolute_uri('/')
                path = f'ads/{pk}'
                ad_path = f'{url}{path}'

                logger.info(f'Returning initial swish-payment template to user with pk {request.user.pk} for ad with pk {pk}')

                return render(
                    request, 
                    'core/payment/swish_payment_template.html', 
                    {
                        'pk': pk, 
                        'title': ad_title, 
                        'price': CURRENT_PRICE_STRING, 
                        'ad_path': ad_path
                    }
                )
        

            if 'swish-pay/extend' in url:

                try: 
                    ad_obj = Advertisement.objects.get(pk=pk)
                except Advertisement.DoesNotExist():
                    logger.exception(f'Failed to return Advertisement which couldnt be found when user with PK {request.user-pk} requested extended swish payment template')
                    return HttpResponseNotFound("Annonsen kunde inte hittas")  

                if not ad_obj.has_initial_payment:
                    return HttpResponseRedirect(reverse_lazy('ad_detail', kwargs={'pk': pk}))


                ad_title = ad_obj.title

                url = request.build_absolute_uri('/')
                path = f'ads/{pk}'
                ad_path = f'{url}{path}'

                current_end_date = ad_obj.deletion_date
                new_end_date = current_end_date + datetime.timedelta(days=30)

                current_end_date_sv = current_end_date.strftime("%a, %d %b %Y")
                new_end_date_sv = new_end_date.strftime("%a, %d %b %Y")

                logger.info(f'Returning extended swish-payment template to user with pk {request.user.pk} for ad with pk {pk}')

                return render(
                    request, 
                    'core/payment/swish_payment_template.html', 
                    {
                        'pk': pk, 
                        'title': ad_title, 
                        'price': CURRENT_PRICE_STRING, 
                        'ad_path': ad_path,
                        'current_end_date': current_end_date_sv,
                        'new_end_date': new_end_date_sv,
                    }
                )
    
        else:
            return redirect('account_login')


class PayForAdBg(View):
    """ 
    Generate template for user for paying with Bankgiro.
    """

    def get(self, request, pk):
        if request.user.is_authenticated:
            CURRENT_PRICE, CURRENT_PRICE_STRING = get_current_ad_price_as_int_and_string()

            # Handle price depending on if it's an initial/extened payment
            PRICE_TO_PAY = CURRENT_PRICE_STRING

            try: 
                ad_obj = Advertisement.objects.get(pk=pk)
            except Advertisement.DoesNotExist():
                return HttpResponseNotFound("Annonsen kunde inte hittas")  

            if ad_obj.has_initial_payment:
                PRICE_TO_PAY = CURRENT_PRICE_STRING

            url = request.build_absolute_uri('/')
            path = f'ads/{pk}'
            ad_path = f'{url}{path}'

            logger.info(f'Returning BG payment template to user with pk {request.user.pk} for ad with {pk}')
            return render(request, 'core/payment/bg_instructions.html', {'pk': pk, 'price': PRICE_TO_PAY, 'ad_path': ad_path})
        else:
            return redirect('account_login')









