import datetime
import io
from re import template
from wsgiref import validate
import qrcode 
import json
import requests
import json
from urllib.parse import urljoin
from pprint import pprint 
import locale

from django.http.response import HttpResponseNotFound, HttpResponseRedirect, JsonResponse
from django.views import generic
from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import generic
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.utils.safestring import mark_safe
from django.forms import HiddenInput, ValidationError
from django.contrib.auth import get_user, get_user_model
from django.db.models import F
from django.template.loader import render_to_string
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist



from dal import autocomplete
from lockdown.decorators import lockdown
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Field, Row, Column, HTML, Div
from crispy_forms.bootstrap import (
    PrependedText, PrependedAppendedText, FormActions, InlineRadios, InlineCheckboxes)

from core.forms import NewAdTakeMyDogForm, NewAdGetMeADogForm
from core.models import Advertisement, Province, Municipality, Area, DogBreed, DogSizeChoice, Payment, NewsEmail, get_30_days_ahead_from_date_obj, get_30_days_ahead
from core.forms import NewsEmailForm, SearchAllAdsForm, SearchOfferingDogAdsForm, SearchRequestingDogAdsForm
from kontorshund.settings import PRICE_SWISH_EXTEND_IN_SEK, PRICE_SWISH_EXTEND, PRICE_BANKGIRO_INITIAL, PRICE_SWISH_INITIAL, PRICE_SWISH_INITIAL_IN_SEK, SWISH_PAYEEALIAS, SWISH_URL, SWISH_CERT, SWISH_ROOTCA, NGROK_URL
from core.filters import AdOfferingDogFilter

User = get_user_model()

locale.setlocale(locale.LC_ALL,'sv_SE.UTF-8')


def template_preview(request):

    url = request.build_absolute_uri('/')
    ad_root_path = f'{url}ads/'

    all_ads = Advertisement.objects.all()
    news_email_uuid = '1198e1f8-e877-4ee3-8024-fbadd246d769'

    context = {
        'ads': all_ads,
        'ad_root_path': ad_root_path,
        'province': 'Stockholm',
        'municipality': 'Stockholms stad',
        'area': 'Sköndal',
        'ad_type': 'Hund sökes',
        'news_email_uuid': news_email_uuid,

    }

    return render(request, 'core/subscription_email/daily_mail.html', context=context)


def deactivate_news_email_subscription(request, uuid):


    if request.method == 'GET':

        print(uuid)
        context = {
            'uuid': uuid
        }
        return render(request, 'core/subscription_email/deactivate_subscription.html', context=context)


    if request.method == 'POST':

        try:
            news_email_obj = NewsEmail.objects.get(uuid=uuid)
            news_email_obj.is_active = False
            news_email_obj.save()

        except:
            return render(request, 'core/subscription_email/subscription_deactivation_error.html')

        return render(request, 'core/subscription_email/subscription_deactivated_confirmation.html')




#############
# INDEX VIEW
#############

@lockdown()
def index(request):
    return render(request, 'core/index.html')


###############
# reCAPCHA view
###############

def recapcha(request, pk):
    payload=request.body
    data_dict = json.loads(payload.decode("utf-8"))
    recaptcha_response = data_dict['token']
    import os

    data = {
      'secret': os.environ.get('reCAPTCHA_SECRET_KEY'),
      'response': recaptcha_response
      }


    print(data)
      
    
    response = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
    result = json.loads(response.text)

    if result['success']:
        email = Advertisement.objects.get(pk=pk).author.email
        return JsonResponse(email, status=200, safe=False)
    
    else:
        return JsonResponse('Not validated', status=403, safe=False)


#####################
# USER SPECIFIC VIEWS
#####################


def profile(request):

    if request.user.is_authenticated:

        url = request.build_absolute_uri('/')
        media_url = f'{url}media/'
        ad_url = f'{url}ads/'
        
        if request.method == 'GET':

            published_ads = Advertisement.objects.filter(author=request.user, is_published=True)
            unpublished_ads = Advertisement.objects.filter(author=request.user, is_published=False)
            deleted_ads = Advertisement.objects.filter(author=request.user, is_deleted=True)
            NewsEmail_obj = NewsEmail.objects.get(user=request.user)
            form = NewsEmailForm(instance=NewsEmail_obj)


            return render(
                request, 
                'core/profile.html', 
                    {
                        'published_ads': published_ads, 
                        'unpublished_ads': unpublished_ads, 
                        'deleted_ads': deleted_ads,
                        'media_url': media_url,
                        'ad_url': ad_url,
                        'form': form,
                        'news_email_obj': NewsEmail_obj,
                }
            )
        if request.method == 'POST':
            NewsEmail_obj = NewsEmail.objects.get(user=request.user)
            form = NewsEmailForm(request.POST, instance=NewsEmail_obj)

            if form.is_valid():
                form.save()
                return redirect('profile')
            else:
                return render(request, 'core/profile.html', {'form': form})
    else:
        return redirect('account_login')



def handle_email_subscription_status(self, uuid):
    NewsEmail_obj = NewsEmail.objects.get(uuid=uuid)

    if NewsEmail_obj.is_active == False:
        NewsEmail_obj.is_active = True
        NewsEmail_obj.save()
        return JsonResponse("Activated", status=200, safe=False)
    else:
        NewsEmail_obj.is_active = False
        NewsEmail_obj.save()
        return JsonResponse("Deactivated", status=200, safe=False)



########################
# VIEWS FOR AUTOCOMPLETE
########################

class BreedAutocomplete(autocomplete.Select2QuerySetView):

    def get_queryset(self):

        if not self.request.user.is_authenticated:
            return DogBreed.objects.none()

        qs = DogBreed.objects.all()

        if self.q:
            qs = qs.filter(name__icontains=self.q)

        return qs

#######################
# VIEWS FOR LISTING ADS 
#######################

def is_search_object_empty(self):
    if self == {}:
        return False
    if self == '':
        return False
    if '--' in self:
        return False
    return True

def ListAndSearchAdsView(request):

    if request.method == 'GET':
        count_all_ads = Advertisement.get_all_active_ads().count()
        count_all_offering_ads = Advertisement.get_all_active_offering_ads().count()
        count_all_requesting_ads = Advertisement.get_all_active_requesting_ads().count()

        context = {
            'count_all_ads': count_all_ads,
            'count_all_offering_ads': count_all_offering_ads,
            'count_all_requesting_ads': count_all_requesting_ads,
        }

        return render(request, 'core/list_ads.html', context=context)

    if request.method == 'POST':
        body_json = json.loads(request.body)

        province_str = body_json['province'][:-7]
        municipality_str = body_json['municipality'][:-7]
        area_str = body_json['area'][:-7]
        type_of_ad_str= body_json['type_of_ad']
        size_offered_list_str = body_json['size_offered']
        size_requested_list_str = body_json['size_requested']
        days_per_week_list_str = body_json['days_per_week']
        OFFSET = body_json['offset']


        province = ''
        municipality = ''
        area = ''
        size_offered_obj_list = []
        size_requested_obj_list = []
        type_of_ad = ''
        days_per_week = ''


        if is_search_object_empty(province_str):
            try:
                province = Province.objects.get(name=province_str)
            except Province.DoesNotExist():
                print('error')

        if is_search_object_empty(municipality_str):
            try:
                municipality = Municipality.objects.get(name=municipality_str)
            except Municipality.DoesNotExist():
                raise ValidationError

        if is_search_object_empty(area_str):
            try:
                area = Area.objects.get(name=area_str)
            except Area.DoesNotExist():
                raise ValidationError

        if is_search_object_empty(size_offered_list_str):
            for size in size_offered_list_str:
                try:
                    size_offered_obj_list.append(DogSizeChoice.objects.get(size=size)) 
                except DogSizeChoice.DoesNotExist():
                    raise ValidationError

        if is_search_object_empty(size_requested_list_str):
            for size in size_requested_list_str:
                try:
                    size_requested_obj_list.append(DogSizeChoice.objects.get(size=size)) 
                except DogSizeChoice.DoesNotExist():
                    raise ValidationError


        ads = ''

        field_value_pairs = [
            ('province', province), 
            ('municipality', municipality),
            ('area', area),
            ('days_per_week__in', days_per_week_list_str),
            ('size_offered__in', size_offered_obj_list),
            ('size_requested__in', size_requested_obj_list),
        ]

        filter_options = {k:v for k,v in field_value_pairs if v}


        # PAGINATED RESPONSE

        TOTAL = 10 # Articles to load per request
        #OFFSET = request.GET.get('offset', 0)
        END = OFFSET + TOTAL
        
        # to understand OFFSET and END, consider this:
        # mylist = [1,2,3,4,5,6,7,8,9]
        # mylist[2:5] outputs => [3,4,5]
        # Above 2 is OFFSET and 5 is END

        # GENERATE QUERYSET

        if type_of_ad_str == 'all':
            qs = Advertisement.objects.filter(
                **filter_options, 
                is_published=True, 
                is_deleted=False
            ).order_by('pk')
            qs_length = qs.count()
            ads = qs[OFFSET:END]

        if type_of_ad_str == 'offering':
            qs = Advertisement.objects.filter(
                **filter_options, 
                is_published=True, 
                is_deleted=False, 
                is_offering_own_dog=True
            ).order_by('pk')
            qs_length = qs.count()
            ads = qs[OFFSET:END]
        if type_of_ad_str == 'requesting':
            qs = Advertisement.objects.filter(
                **filter_options, 
                is_published=True, 
                is_deleted=False, 
                is_offering_own_dog=False
            ).order_by('pk')
            qs_length = qs.count()
            ads = qs[OFFSET:END]

        json_dict = {}
        json_dict['ads'] = []

        for ad in ads:
            json_dict['ads'].append(
                {
                'pk': ad.pk,
                'title': ad.title, 
                'image_url': ad.image1.url,
                'is_offering_own_dog': ad.is_offering_own_dog,
                'province': ad.province.name,
                'municipality': ad.municipality.name,
                'days_per_week': ad.days_per_week,
                **({'area': ad.area.name} if ad.area else {})
                }
            )

        json_dict['total_ads'] = qs_length

        data = json.dumps(json_dict)



        return JsonResponse(data, status=200, safe=False)



class AdOfferingDogListView(generic.ListView):
    
    model = Advertisement
    context_object_name = 'ads'
    template_name = 'core/advertisement_list_offering_dog.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = AdOfferingDogFilter(self.request.GET, queryset=self.get_queryset())
        return context

    def get_queryset(self):
        queryset = Advertisement.objects.filter(is_offering_own_dog=True, is_published=True, is_deleted=False)
        return queryset


class AdListGetMeADog(generic.ListView):
    model = Advertisement
    context_object_name = 'ads'
    template_name = 'core/advertisement_list_get.html'

    def get_queryset(self):
        queryset = Advertisement.objects.filter(is_offering_own_dog=False)
        return queryset

#############################
# VIEWS FOR HANDLING PAYMENTS 
#############################


def check_initial_payment_status(request, pk):
    if request.user.is_authenticated:
        try:
            ad = Advertisement.objects.get(pk=pk)
        except Advertisement.DoesNotExist:
            return JsonResponse("Ad does not exist", status=404, safe=False)

        if ad.has_initial_payment:
            return JsonResponse("Payment is complete!", status=200, safe=False)
        else:
            return JsonResponse("Payment is NOT complete", status=404, safe=False)
    else:
        return redirect('account_login')

def check_extended_payment_status(request, pk):
    if request.user.is_authenticated:
        try:
            ad = Advertisement.objects.get(pk=pk)
        except Advertisement.DoesNotExist:
            return JsonResponse("Ad does not exist", status=404, safe=False)

        if ad.has_extended_payment:
            return JsonResponse("Payment is complete!", status=200, safe=False)
        else:
            return JsonResponse("Payment is NOT complete", status=404, safe=False)
    else:
        return redirect('account_login')


def android_success_page(request):
    return render(request, 'android_swish_success.html')

from django.db import transaction


@csrf_exempt
def swish_callback(request):

    print("******************")
    print("Swish Callback ***", flush=True)

    data=request.body
    data_dict = json.loads(data.decode("utf-8"))
    pprint(data_dict)

    # Check if payment was successfull
    if data_dict['status'] == 'PAID':

        ad_id = data_dict['payeePaymentReference']
        amount = data_dict['amount']
        date_paid_str = data_dict['datePaid']
        date_paid_obj = datetime.datetime.strptime(date_paid_str, '%Y-%m-%dT%H:%M:%S.%f%z')
        payment_reference = data_dict['paymentReference']
        payer_alias = data_dict['payerAlias']


        try:
            ad_obj = Advertisement.objects.get(pk=ad_id) # Make sure that the count when adding an ad is correct and not prone to race conditions
        except Advertisement.DoesNotExist:
            return JsonResponse("Annonsen hittades ej", status=404, safe=False)


        # If payment is extended
        if ad_obj.has_initial_payment:

            payment_obj = ad_obj.create_payment(
                payment_type=2, 
                amount=amount, 
                payment_reference=payment_reference,
                date_time_paid = date_paid_obj,
                payer_alias = payer_alias
                )

            ad_obj.is_published = True
            ad_obj.is_deleted = False


            # Base case - add 30 day ahead from today (if ad already has passed deletion date)
            new_deletion_date = get_30_days_ahead()

            # If deletion date is later than today, add 30 days ontop of that
            if get_30_days_ahead_from_date_obj(ad_obj.deletion_date) > new_deletion_date:
                new_deletion_date = get_30_days_ahead_from_date_obj(ad_obj.deletion_date)

            ad_obj.deletion_date = new_deletion_date
            ad_obj.save()

            print(f'Payment created, payment id {payment_obj.pk}')
            return JsonResponse(f"Payment was created, id: {payment_obj.pk}", status=201, safe=False)

        # If payment is initial
        else:

            payment_obj = ad_obj.create_payment(
                payment_type=1, 
                amount=amount, 
                payment_reference=payment_reference,
                date_time_paid = date_paid_obj,
                payer_alias = payer_alias
                )

            ad_obj.is_published = True

            if ad_obj.area:
                ad_obj.area.count = F('count') + 1        
            
            ad_obj.save()

            print(f'Payment created, payment id {payment_obj.pk}')

            return JsonResponse(f"Payment was created, id: {payment_obj.pk}", status=201, safe=False)

    else:

        error_code = data_dict['errorCode']
        error_message = data_dict['errorCode']

        print(f'Problem creating payment: {error_code} {error_message}')
        return JsonResponse(f"Payment couldn't be created: {error_code} {error_message}", status=401, safe=False)



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

        #img = qr.make_image(fill='black', back_color='white')
        #img.save('qrcode001.png')

        bytesio_object = io.BytesIO()
        qr_img.save(bytesio_object)

        file_data = bytesio_object.getvalue()
        response = HttpResponse(content_type=f'image/png')
        response['Content-Disposition'] = f'inline; filename="qr-code-image"'
        response.write(file_data)

        return response 
    else:
        return redirect('account_login')


def PayForAdSwishTemplate(request, pk):
    if request.user.is_authenticated:

        url = request.build_absolute_uri()

        if 'swish-pay/initial' in url:
        
            try: 
                ad_obj = Advertisement.objects.get(pk=pk)
            except Advertisement.DoesNotExist():
                return HttpResponseNotFound("Annonsen kunde inte hittas")     

            if ad_obj.has_initial_payment:
                return HttpResponseRedirect(reverse_lazy('ad_detail', kwargs={'pk': pk}))


            ad_title = ad_obj.title
            url = request.build_absolute_uri('/')
            path = f'ads/{pk}'
            ad_path = f'{url}{path}'
            return render(
                request, 
                'core/swish_payment_template.html', 
                {
                    'pk': pk, 
                    'title': ad_title, 
                    'price': PRICE_SWISH_INITIAL, 
                    'ad_path': ad_path
                }
            )
    

        if 'swish-pay/extend' in url:

            try: 
                ad_obj = Advertisement.objects.get(pk=pk)
            except Advertisement.DoesNotExist():
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


            return render(
                request, 
                'core/swish_payment_template.html', 
                {
                    'pk': pk, 
                    'title': ad_title, 
                    'price': PRICE_SWISH_EXTEND, 
                    'ad_path': ad_path,
                    'current_end_date': current_end_date_sv,
                    'new_end_date': new_end_date_sv,
                }
            )
   
    else:
        return redirect('account_login')




def GenerateSwishPaymentRequestToken(request, pk):


    if request.user.is_authenticated:


        # Handle price depending on if it's an initial/extened payment
        PRICE_TO_PAY = PRICE_SWISH_INITIAL_IN_SEK

        try: 
            ad_obj = Advertisement.objects.get(pk=pk)
        except Advertisement.DoesNotExist():
            return HttpResponseNotFound("Annonsen kunde inte hittas")  

        if ad_obj.has_initial_payment:
            PRICE_TO_PAY = PRICE_SWISH_EXTEND_IN_SEK
        else:
            PRICE_TO_PAY = PRICE_SWISH_INITIAL_IN_SEK
                
        # Enable for local testing
        #SWISH_CALLBACKURL = urljoin(NGROK_URL, "/swish/callback")

        url = request.build_absolute_uri('/')
        callback_path = f'swish/callback'
        # Enable for prod
        SWISH_CALLBACKURL= f'{url}{callback_path}'

        print(SWISH_CALLBACKURL, flush=True)

        # Set-up variables for payment request
        payload = {
            "payeePaymentReference": pk,
            "callbackUrl": SWISH_CALLBACKURL,
            "payeeAlias": SWISH_PAYEEALIAS,
            #"payerAlias": phone_number_with_46,    # Payers phone number
            "currency": "SEK",
            "amount": PRICE_TO_PAY,
            "message": f"Betalning för annons med ID {pk}"
        }

        resp = requests.post(urljoin(SWISH_URL, "v1/paymentrequests"), json=payload, cert=SWISH_CERT, verify=SWISH_ROOTCA, timeout=2)
        print(resp.status_code, resp.text, resp.headers)
        PaymentRequestToken = resp.headers['PaymentRequestToken']

        return JsonResponse({'token': PaymentRequestToken, 'callback_url': SWISH_CALLBACKURL}, status=201, safe=False)
    else:
        return redirect('account_login')




def GenerateSwishPaymentQrCode(request, pk):

    if request.user.is_authenticated:

        # Handle price depending on if it's an initial/extened payment
        PRICE_TO_PAY = PRICE_SWISH_INITIAL_IN_SEK

        try: 
            ad_obj = Advertisement.objects.get(pk=pk)
        except Advertisement.DoesNotExist():
            return HttpResponseNotFound("Annonsen kunde inte hittas")  

        if ad_obj.has_initial_payment:
            PRICE_TO_PAY = PRICE_SWISH_EXTEND_IN_SEK
        else:
            PRICE_TO_PAY = PRICE_SWISH_INITIAL_IN_SEK


        # Enable for local testing
        #SWISH_CALLBACKURL = urljoin(NGROK_URL, "/swish/callback")

        url = request.build_absolute_uri('/')
        callback_path = f'swish/callback'
        # Enable for prod
        SWISH_CALLBACKURL= f'{url}{callback_path}'

        # Set-up variables for payment request
        payload = {
            "payeePaymentReference": pk,
            "callbackUrl": SWISH_CALLBACKURL,
            "payeeAlias": SWISH_PAYEEALIAS,
            #"payerAlias": phone_number_with_46,    # Payers phone number
            "currency": "SEK",
            "amount": PRICE_TO_PAY,
            "message": f"Betalning för annons med ID {pk}"
        }

        resp = requests.post(urljoin(SWISH_URL, "v1/paymentrequests"), json=payload, cert=SWISH_CERT, verify=SWISH_ROOTCA, timeout=2)
        print(resp.status_code, resp.text, resp.headers)
        PaymentRequestToken = resp.headers['PaymentRequestToken']

        qr_image_response = get_qr_code(request, PaymentRequestToken)


        return qr_image_response
    else:
        return redirect('account_login')


def PayForAdBG(request, pk):
    if request.user.is_authenticated:

        # Handle price depending on if it's an initial/extened payment
        PRICE_TO_PAY = PRICE_SWISH_INITIAL_IN_SEK

        try: 
            ad_obj = Advertisement.objects.get(pk=pk)
        except Advertisement.DoesNotExist():
            return HttpResponseNotFound("Annonsen kunde inte hittas")  

        if ad_obj.has_initial_payment:
            PRICE_TO_PAY = PRICE_SWISH_EXTEND_IN_SEK
        else:
            PRICE_TO_PAY = PRICE_SWISH_INITIAL_IN_SEK


        url = request.build_absolute_uri('/')
        path = f'ads/{pk}'
        ad_path = f'{url}{path}'

        if request.method == "GET":
            # Generate template to fill in your phone number
            return render(request, 'bg_instructions.html', {'pk': pk, 'price': PRICE_TO_PAY, 'ad_path': ad_path})
    else:
        return redirect('account_login')

########################
# VIEWS FOR CREATING ADS 
########################

def ChooseAd(request):
    if request.user.is_authenticated:
        return render(request, 'core/choose_ad_type.html')
    else:
        return redirect('account_login')


class NewAdTakeMyDog(LoginRequiredMixin, CreateView):
    model = Advertisement
    form_class = NewAdTakeMyDogForm
    template_name = 'core/advertisement_form_take.html'
    success_url = reverse_lazy('view_ads_take_my_dog')
    login_url = '/accounts/login'

    def __init__(self):
        self.pk = None

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.helper = FormHelper()
        form.helper.add_input(Submit('submit', 'Gå till betalning', css_class='btn-primary'))
      
        form.helper.layout = Layout(
            Field(HTML(mark_safe('<b>Plats</b>'))),  
            Div(
                Field('province', css_class="mb-3"),
                Field('municipality', css_class="mb-3"),
                Field('area', css_class=""),
                css_class='mt-3 mb-5'
            ),
            Field(HTML(mark_safe('<b>Om hunden</b>'))),  
            Div(
                Field('name', css_class="mb-4"),
                Field('age', css_class="mb-4"),
                Field('hundras', css_class="mb-4"),
                InlineRadios('size_offered', css_class="ml-3 mr-2"),
                css_class='mt-3 mb-5'
            ),
            Field(HTML(mark_safe('<b>Annonsen</b>'))),  
            Div(
                Field('title', css_class="mb-4"),
                Field('description', css_class=""),
                css_class='mt-3 mb-5'
            ),
            Div(
                InlineRadios('days_per_week', css_class="ml-3 mr-2"),
                css_class='mt-3 mb-5'
            ),
            Field(HTML(mark_safe('<b>Bilder</b>'))),  
            Div(
                Field('image1', css_class="btn btn-sm mb-4"),
                Field('image2', css_class="btn btn-sm mb-4"),
                Field('image3', css_class="btn btn-sm"),
                css_class='mt-3 mb-5'
            ),

            Field(HTML(mark_safe('<b>Betalning</b>'))),  
            Div(
                InlineRadios('payment_type', css_class="ml-3 mr-2"),
                css_class='mt-3 mb-5'
            ),
        )
        return form

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.is_offering_own_dog = True
        form.instance.is_published = False
        response = super().form_valid(form)
        return response

    def get_success_url(self):
        if self.object.payment_type == 'S':
            return reverse('swish_payment_initial_template', kwargs={'pk': self.object.pk})
        if self.object.payment_type == 'B':
            return reverse('bg_payment', kwargs={'pk': self.object.pk})


class NewAdGetMeADog(CreateView):
    model = Advertisement
    form_class = NewAdGetMeADogForm
    success_url = reverse_lazy('ad_changelist')
    template_name = 'core/advertisement_form_get.html'

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.helper = FormHelper()
        form.fields['image1'].label = False
        form.fields['image2'].label = False
        form.fields['image3'].label = False
        form.helper.add_input(Submit('submit', 'Gå till betalning', css_class='btn-primary'))
      
        form.helper.layout = Layout(
            Field(HTML(mark_safe('<b>Plats</b>'))),  
            Div(
                Field('province', css_class="mb-3"),
                Field('municipality', css_class="mb-3"),
                Field('area', css_class=""),
                css_class='mt-3 mb-5'
            ),
            Field(HTML(mark_safe('<b>Annonsen</b>'))),  
            Div(
                Field('title', css_class="mb-1"),
                Field('description', css_class="mt-2"),
                css_class='mb-5 mt-3'
            ),
            Div(
                InlineCheckboxes('size_requested', css_class="mb-4 ml-3 mr-2"),
                InlineRadios('days_per_week', css_class="ml-3 mr-2"),
                css_class='mb-5 mt-3'
            ),  
            Field(HTML(mark_safe('<b>Bilder</b>'))),  
            Div(
                Field('image1', css_class="btn btn-sm mb-4"),
                Field('image2', css_class="btn btn-sm mb-4"),
                Field('image3', css_class="btn btn-sm"),
                css_class='mt-3 mb-5'
            ),

            Field(HTML(mark_safe('<b>Betalning</b>'))),  
            Div(
                InlineRadios('payment_type', css_class="ml-3 mr-2"),
                css_class='mt-3 mb-5'
            ),
        )
        return form

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.is_offering_own_dog = False
        form.instance.is_published = False
        response = super().form_valid(form)
        return response

    def get_success_url(self):
        if self.object.payment_type == 'S':
            return reverse('swish_payment_initial_template', kwargs={'pk': self.object.pk})
        if self.object.payment_type == 'B':
            return reverse('bg_payment', kwargs={'pk': self.object.pk})

########################
# VIEWS FOR UPDATING ADS 
########################


class AdUpdateTakeMyDogView(UpdateView):
    model = Advertisement
    form_class = NewAdTakeMyDogForm
    template_name = 'core/advertisement_form_update_take.html'

    def get_success_url(self):
        return reverse_lazy('ad_detail', kwargs={'pk': self.object.pk})

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.is_offering_own_dog == False:
            return HttpResponseRedirect(reverse_lazy('ad_update_get', kwargs={'pk': self.object.pk}))
        return super().get(request, *args, **kwargs)


    def get_form(self, form_class=None):
        
        form = super().get_form(form_class)
        form.helper = FormHelper()
        form.helper.add_input(Submit('submit', 'Spara och gå tillbaka till annonsen', css_class='btn-primary'))
        payment_header = ''
        if form.instance.is_published:
            form.fields['payment_type'].widget = HiddenInput()
            payment_header = ''
        else:
            payment_header = '<b>Betalning</b>'
        form.helper.layout = Layout(
            Field(HTML(mark_safe('<b>Plats</b>'))),  
            Div(
                Field('province', css_class="mb-3"),
                Field('municipality', css_class="mb-3"),
                Field('area', css_class=""),
                css_class='mt-3 mb-5'
            ),
            Field(HTML(mark_safe('<b>Om hunden</b>'))),  
            Div(
                Field('name', css_class="mb-4"),
                Field('age', css_class="mb-4"),
                Field('hundras', css_class="mb-4"),
                InlineRadios('size_offered', css_class="ml-3 mr-2"),
                css_class='mt-3 mb-5'
            ),
            Field(HTML(mark_safe('<b>Annonsen</b>'))),  
            Div(
                Field('title', css_class="mb-4"),
                Field('description', css_class=""),
                css_class='mt-3 mb-5'
            ),
            Div(
                InlineRadios('days_per_week', css_class="ml-3 mr-2"),
                css_class='mt-3 mb-5'
            ),
            Field(HTML(mark_safe('<b>Bilder</b>'))),  
            Div(
                Field('image1', css_class="btn btn-sm mb-4"),
                Field('image2', css_class="btn btn-sm mb-4"),
                Field('image3', css_class="btn btn-sm"),
                css_class='mt-3 mb-5'
            ),

            Field(HTML(mark_safe(payment_header))),  
            Div(
                InlineRadios('payment_type', css_class="ml-3 mr-2"),
                css_class='mt-3 mb-5'
            ),
        )
        return form


class AdUpdateGetMeADogView(UpdateView):
    model = Advertisement
    form_class = NewAdGetMeADogForm
    template_name = 'core/advertisement_form_update_get.html'


    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.is_offering_own_dog == True:
            return HttpResponseRedirect(reverse_lazy('ad_update_take', kwargs={'pk': self.object.pk}))
        return super().get(request, *args, **kwargs)

    def get_success_url(self):
        return reverse("ad_detail", kwargs={'pk': self.object.pk})
        #return reverse_lazy('ad_detail', {'pk': self.object.pk})

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.helper = FormHelper()
        form.fields['image1'].label = False
        form.fields['image2'].label = False
        form.fields['image3'].label = False
        payment_header = ''
        if form.instance.is_published:
            form.fields['payment_type'].widget = HiddenInput()
            payment_header = ''
        else:
            payment_header = '<b>Betalning</b>'
        form.helper.add_input(Submit('submit', 'Spara och gå tillbaka till annonsen', css_class='btn-primary'))
      
        form.helper.layout = Layout(
            Field(HTML(mark_safe('<b>Plats</b>'))),  
            Div(
                Field('province', css_class="mb-3"),
                Field('municipality', css_class="mb-3"),
                Field('area', css_class=""),
                css_class='mt-3 mb-5'
            ),
            Field(HTML(mark_safe('<b>Annonsen</b>'))),  
            Div(
                Field('title', css_class="mb-1"),
                Field('description', css_class="mt-2"),
                css_class='mb-5 mt-3'
            ),
            Div(
                InlineCheckboxes('size_requested', css_class="mb-4 ml-3 mr-2"),
                InlineRadios('days_per_week', css_class="ml-3 mr-2"),
                css_class='mb-5 mt-3'
            ),  
            Field(HTML(mark_safe('<b>Bilder</b>'))),  
            Div(
                Field('image1', css_class="btn btn-sm mb-4"),
                Field('image2', css_class="btn btn-sm mb-4"),
                Field('image3', css_class="btn btn-sm"),
                css_class='mt-3 mb-5'
            ),

            Field(HTML(mark_safe(payment_header))),  
            Div(
                InlineRadios('payment_type', css_class="ml-3 mr-2"),
                css_class='mt-3 mb-5'
            ),
        )
        return form


########################
# VIEWS FOR VIEWING ADS
########################

class AdDetailView(generic.DetailView):
    model = Advertisement
    context_object_name = 'ad'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.ad_views = self.object.ad_views + 1
        self.object.save()
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(AdDetailView, self).get_context_data(**kwargs)
        context['site_key'] = settings.RECAPTCHA_SITE_KEY
        context['price_swish_extend'] = PRICE_SWISH_EXTEND
        return context


########################
# VIEWS FOR DELETING ADS 
########################

class DeleteAd(generic.DeleteView):
    model = Advertisement
    template_name = 'core/ad_confirm_delete.html'
    success_url = reverse_lazy('profile')


###################
# GEOGRAPHIES VIEWS
###################


# View to be used for getting Municipalities connected to a Province

def load_provinces(request):
   # province_id = request.headers['province']
    provinces = list(Province.objects.all().values('id', 'name', 'offering_count', 'requesting_count').order_by('name'))
    return HttpResponse(json.dumps(provinces), content_type="application/json") 

def load_municipalities(request):
   # province_id = request.headers['province']
    province_id = request.GET.get('province','') 
    municipalities = list(Municipality.objects.filter(province_id=province_id).values('id', 'name', 'offering_count', 'requesting_count').order_by('name'))
    return HttpResponse(json.dumps(municipalities), content_type="application/json") 

# View to be used for getting Areas connected to a Municipality
def load_areas(request):
    #municipality_id = request.headers['municipality']
    municipality_id = request.GET.get('municipality','') 
    areas = list(Area.objects.filter(municipality_id=municipality_id).values('id', 'name', 'offering_count', 'requesting_count').order_by('name'))
    return HttpResponse(json.dumps(areas), content_type="application/json") 
