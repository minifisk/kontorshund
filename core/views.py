from django.core.checks import messages
from django.http.response import HttpResponseRedirect, JsonResponse
from django.views import generic
from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import generic
from django.core.files.storage import FileSystemStorage
from django.urls import reverse

from kontorshund.settings import PRICE_BANKGIRO, PRICE_SWISH, PRICE_SWISH_IN_SEK, SWISH_PAYEEALIAS, SWISH_URL, SWISH_CERT, SWISH_ROOTCA, NGROK_URL

import datetime
import io
import qrcode 
import json
import os
from dal import autocomplete
import requests
import json
from urllib.parse import urljoin
from django.views.decorators.csrf import csrf_exempt
from pprint import pprint 


from core.forms import NewAdTakeMyDogForm, NewAdGetMeADogForm, PhoneNumberForm
from core.models import Advertisement, Municipality, Area, DogBreeds, Payment

# Create your views here.

def index(request):
    return render(request, 'core/index.html')


def testindex(request):
    return JsonResponse("Kontorshund.se kommer i februari 2022 - Annonsplatsen d'a'r du kan erbjuda eller s'o'ka en kontorshund!", status=404, safe=False)


def ChooseAd(request):
    return render(request, 'core/choose_ad_type.html')

def ListAds(request):
    return render(request, 'core/list_ads.html')


def check_payment_status(request, pk):
    try:
        ad = Advertisement.objects.get(pk=pk)
    except Advertisement.DoesNotExist:
        return JsonResponse("Ad does not exist", status=404, safe=False)

    if ad.has_initial_payment():
        return JsonResponse("Payment is complete!", status=200, safe=False)
    else:
        return JsonResponse("Payment is NOT complete", status=404, safe=False)


def android_success_page(request):
    return render(request, 'android_swish_success.html')


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
            ad_object = Advertisement.objects.get(pk=ad_id)
        except Advertisement.DoesNotExist:
            return JsonResponse("Ad does not exist", status=404, safe=False)

        payment_obj = ad_object.create_payment(
            payment_type=1, 
            amount=amount, 
            payment_reference=payment_reference,
            date_time_paid = date_paid_obj,
            payer_alias = payer_alias
            )

        print(f'Payment created, payment id {payment_obj.pk}')

        return JsonResponse(f"Payment was created, id: {payment_obj.pk}", status=201, safe=False)

    else:

        error_code = data_dict['errorCode']
        error_message = data_dict['errorCode']


        print(f'Problem creating payment: {error_code} {error_message}')
        return JsonResponse(f"Payment couldn't be created: {error_code} {error_message}", status=401, safe=False)



def get_qr_code(token):

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



class BreedAutocomplete(autocomplete.Select2QuerySetView):

    def get_queryset(self):

        #if not self.request.user.is_authenticated:
        #    return DogBreeds.objects.none()

        qs = DogBreeds.objects.all()

        if self.q:
            qs = qs.filter(name__icontains=self.q)

        return qs


class AdListTakeMyDog(generic.ListView):
    model = Advertisement
    context_object_name = 'ads'
    template_name = 'core/advertisement_list_take.html'

    def get_queryset(self):
        queryset = Advertisement.objects.filter(is_offering_own_dog=True)
        return queryset


class AdListGetMeADog(generic.ListView):
    model = Advertisement
    context_object_name = 'ads'
    template_name = 'core/advertisement_list_get.html'

    def get_queryset(self):
        queryset = Advertisement.objects.filter(is_offering_own_dog=False)
        return queryset


class NewAdTakeMyDog(CreateView):
    model = Advertisement
    form_class = NewAdTakeMyDogForm
    template_name = 'core/advertisement_form_take.html'
    success_url = reverse_lazy('view_ads_take_my_dog')

    def __init__(self):
        self.pk = None

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.is_offering_own_dog = True
        form.instance.is_published = False
        response = super().form_valid(form)
        return response


    def get_success_url(self):
        if self.object.payment_type == 'S':
            return reverse('swish_payment_template', kwargs={'pk': self.object.pk})
        if self.object.payment_type == 'B':
            return reverse('bg_payment', kwargs={'pk': self.object.pk})


def PayForAdSwishTemplate(request, pk):
    ad_title = Advertisement.objects.get(pk=pk).title
    form = PhoneNumberForm()

    return render(request, 'swish_phone_number.html', {'pk': pk, 'form': form, 'title': ad_title, 'price': PRICE_SWISH})


def GenerateSwishPaymentRequestToken(request, pk):

    # SWISH_CALLBACKURL = urljoin(NGROK_URL, "/swish/callback")

    url = request.build_absolute_uri('/')
    callback_path = f'swish/callback'
    SWISH_CALLBACKURL= f'{url}{callback_path}'

    print(SWISH_CALLBACKURL, flush=True)

    # Set-up variables for payment request
    payload = {
        "payeePaymentReference": pk,
        "callbackUrl": SWISH_CALLBACKURL,
        "payeeAlias": SWISH_PAYEEALIAS,
        #"payerAlias": phone_number_with_46,    # Payers phone number
        "currency": "SEK",
        "amount": PRICE_SWISH_IN_SEK,
        "message": f"Betalning för annons med ID {pk}"
    }

    resp = requests.post(urljoin(SWISH_URL, "v1/paymentrequests"), json=payload, cert=SWISH_CERT, verify=SWISH_ROOTCA, timeout=2)
    print(resp.status_code, resp.text, resp.headers)
    PaymentRequestToken = resp.headers['PaymentRequestToken']

    return JsonResponse({'token': PaymentRequestToken, 'callback_url': SWISH_CALLBACKURL}, status=201, safe=False)





def GenerateSwishPaymentQrCode(request, pk):

    # Generate callback url if development
    if bool(os.environ.get('IS_DEVELOPMENT')) == True:
        SWISH_CALLBACKURL = urljoin(NGROK_URL, "/swish/callback")

    # Generate callback url if production
    if bool(os.environ.get('IS_DEVELOPMENT')) == False:
        url = request.build_absolute_uri('/')
        callback_path = f'swish/callback'
        SWISH_CALLBACKURL= f'{url}{callback_path}'

    # Set-up variables for payment request
    payload = {
        "payeePaymentReference": pk,
        "callbackUrl": SWISH_CALLBACKURL,
        "payeeAlias": SWISH_PAYEEALIAS,
        #"payerAlias": phone_number_with_46,    # Payers phone number
        "currency": "SEK",
        "amount": PRICE_SWISH_IN_SEK,
        "message": f"Betalning för annons med ID {pk}"
    }

    resp = requests.post(urljoin(SWISH_URL, "v1/paymentrequests"), json=payload, cert=SWISH_CERT, verify=SWISH_ROOTCA, timeout=2)
    print(resp.status_code, resp.text, resp.headers)
    PaymentRequestToken = resp.headers['PaymentRequestToken']

    qr_image_response = get_qr_code(PaymentRequestToken)


    return qr_image_response



def PayForAdBG(request, pk):
    url = request.build_absolute_uri('/')
    ad_path = f'ads/{pk}'
    full_path = f'{url}{ad_path}'

    if request.method == "GET":
        # Generate template to fill in your phone number
        return render(request, 'bg_instructions.html', {'pk': pk, 'price': PRICE_BANKGIRO, 'ad_path': full_path})



class NewAdGetMeADog(CreateView):
    model = Advertisement
    form_class = NewAdGetMeADogForm
    success_url = reverse_lazy('ad_changelist')
    template_name = 'core/advertisement_form_get.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.is_offering_own_dog = False
        return super().form_valid(form)


class AdUpdateView(UpdateView):
    model = Advertisement
    form_class = NewAdTakeMyDogForm
    success_url = reverse_lazy('ad_changelist')


class AdDetailView(generic.DetailView):
    model = Advertisement
    context_object_name = 'ad'

# View to be used for getting Municipalities connected to a Province
def load_municipalities(request):
    province_id = request.headers['province']
    municipalities = Municipality.objects.filter(province_id=province_id).order_by('name')
    return render(request, 'municipality_dropdown_list_options.html', {'municipalities': municipalities})

# View to be used for getting Areas connected to a Municipality
def load_areas(request):
    municipality_id = request.headers['municipality']
    areas = Area.objects.filter(municipality_id=municipality_id).order_by('name')
    return render(request, 'area_dropdown_list_options.html', {'areas': areas})
