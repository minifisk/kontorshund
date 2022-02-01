import json
import requests
import json
import locale

from django.http.response import JsonResponse
from django.shortcuts import render
from django.http import HttpResponse

from dal import autocomplete

from core.models import Advertisement, Province, Municipality, Area, DogBreed, NewsEmail

locale.setlocale(locale.LC_ALL,'sv_SE.UTF-8')


####################
# EMAIL SUBSCRIPTION
####################

def deactivate_news_email_subscription(request, uuid):
    if request.method == 'GET':

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
    
    response = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
    result = json.loads(response.text)

    if result['success']:
        email = Advertisement.objects.get(pk=pk).author.email
        return JsonResponse(email, status=200, safe=False)
    
    else:
        return JsonResponse('Not validated', status=403, safe=False)


###############
# AUTOCOPMPLETE
###############

class BreedAutocomplete(autocomplete.Select2QuerySetView):

    def get_queryset(self):

        if not self.request.user.is_authenticated:
            return DogBreed.objects.none()

        qs = DogBreed.objects.all()

        if self.q:
            qs = qs.filter(name__icontains=self.q)

        return qs


###################
# GEOGRAPHIES VIEWS
###################

def load_provinces(request):
    provinces = list(Province.objects.all().values('id', 'name', 'offering_count', 'requesting_count').order_by('name'))
    return HttpResponse(json.dumps(provinces), content_type="application/json") 

def load_municipalities(request):
    province_id = request.GET.get('province','') 
    municipalities = list(Municipality.objects.filter(province_id=province_id).values('id', 'name', 'offering_count', 'requesting_count').order_by('name'))
    return HttpResponse(json.dumps(municipalities), content_type="application/json") 

def load_areas(request):
    municipality_id = request.GET.get('municipality','') 
    areas = list(Area.objects.filter(municipality_id=municipality_id).values('id', 'name', 'offering_count', 'requesting_count').order_by('name'))
    return HttpResponse(json.dumps(areas), content_type="application/json") 
