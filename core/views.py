from django.http.response import HttpResponseRedirect, JsonResponse
from django.views import generic
from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import generic
from django.core.files.storage import FileSystemStorage
from django.urls import reverse

from kontorshund.settings import PRICE_BANKGIRO, PRICE_SWISH, SWISH_PAYEEALIAS, SWISH_URL, SWISH_CERT, SWISH_ROOTCA, NGROK_URL



import os
from dal import autocomplete
import requests
import json
from urllib.parse import urljoin
from django.views.decorators.csrf import csrf_exempt
from pprint import pprint 


from core.forms import NewAdTakeMyDogForm, NewAdGetMeADogForm, PhoneNumberForm
from core.models import Advertisement, Municipality, Area, DogBreeds

# Create your views here.

def index(request):
 
    # NGROK_URL = "https://e40c-92-33-202-136.ngrok.io/"

    # SWISH_CALLBACKURL = urljoin(NGROK_URL, "/swish/callback")

    # SWISH_PAYEEALIAS = os.environ.get('MERCHANT_SWISH_NUMBER') # This would be your merchant swish number in production. In test it doesnt matter

    # SWISH_ROOTCA = "/home/kontorshund/web/Certificates_prod/Swish_TLS_RootCA.pem"
    # SWISH_CERT = ("/home/kontorshund/web/Certificates_prod/swish_certificate_202112151645.pem", "/home/kontorshund/web/Certificates_prod/private.key")

    # #SWISH_URL = "https://mss.cpc.getswish.net/swish-cpcapi/api/"
    # SWISH_URL = "https://cpc.getswish.net/swish-cpcapi/api/" # PRODUCTION


    # payload = {
    #     "payeePaymentReference": "0123456789",
    #     "callbackUrl": SWISH_CALLBACKURL,
    #     "payeeAlias": SWISH_PAYEEALIAS,
    #     "payerAlias": os.environ.get('CUSTOMER_SWISH_NUMBER'),    # Payers (your) phone number
    #     "currency": "SEK",
    #     "amount": "1",
    #     "message": "100-pack plastpåsar"
    # }

    # resp = requests.post(urljoin(SWISH_URL, "v1/paymentrequests"), json=payload, cert=SWISH_CERT, verify=SWISH_ROOTCA, timeout=2)
    # print(resp.status_code, resp.text)

    return render(request, 'core/index.html')


@csrf_exempt
def swish_callback(request):

    print("******************")
    print("Swish Callback ***")

    data=request.body
    data_dict = json.loads(data.decode("utf-8"))
    pprint(data_dict)

    return JsonResponse("This is fine", status=200, safe=False)



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
            return reverse('swish_payment', kwargs={'pk': self.object.pk})
        if self.object.payment_type == 'B':
            return reverse('bg_payment', kwargs={'pk': self.object.pk})


def PayForAdSwish(request, pk):
    if request.method == "GET":
        ad_title = Advertisement.objects.get(pk=pk).title
        form = PhoneNumberForm()

        return render(request, 'swish_phone_number.html', {'form': form, 'title': ad_title, 'price': PRICE_SWISH})

    if request.method == "POST":
        form = PhoneNumberForm(request.POST)
        if form.is_valid():
            
            phone_number = form.cleaned_data['phone_number']
            phone_number_with_46 = f'46{phone_number[1:]}'


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
                "payerAlias": phone_number_with_46,    # Payers phone number
                "currency": "SEK",
                "amount": "1",
                "message": "100-pack plastpåsar"
            }

            resp = requests.post(urljoin(SWISH_URL, "v1/paymentrequests"), json=payload, cert=SWISH_CERT, verify=SWISH_ROOTCA, timeout=2)
            print(resp.status_code, resp.text)

            return render(request, 'swish_phone_number.html', {'form': form, 'title': ad_title, 'price': PRICE_SWISH})

        else:
            ad_title = Advertisement.objects.get(pk=pk).title
            return render(request, 'swish_phone_number.html', {'pk': pk, 'form': form, 'title': ad_title, 'price': PRICE_SWISH})



def PayForAdBG(request, pk):
    from django.contrib.sites.models import Site


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


# def image_upload(request):
#     print("Hello? Anyone there?", flush=True)
#     if request.method == "POST" and request.FILES["image_file"]:
#         image_file = request.FILES["image_file"]
#         fs = FileSystemStorage()
#         filename = fs.save(image_file.name, image_file)
#         image_url = fs.url(filename)
#         print("URL IS:........")
#         print(image_url, flush=True)
#         return render(request, "core/upload.html", {
#             "image_url": image_url
#         })
#     return render(request, "core/upload.html")