import json
from django.views import View
import requests
import json
import locale

from django.http.response import JsonResponse
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, redirect


from dal import autocomplete

from core.models import Advertisement, Province, Municipality, Area, DogBreed, NewsEmail

locale.setlocale(locale.LC_ALL,'sv_SE.UTF-8')

import logging 
logger = logging.getLogger(__name__)


####################
# EMAIL SUBSCRIPTION
####################


class HandleEmailSubscriptionStatus(View):

    def post(self, request, uuid):

        if request.user.is_authenticated:

            NewsEmail_obj = NewsEmail.objects.get(uuid=uuid)

            if NewsEmail_obj.is_active == False:
                NewsEmail_obj.is_active = True
                NewsEmail_obj.save()
                logger.debug(f'Activated NewsEmail subscription for user {request.user.pk}')
                return JsonResponse("Activated", status=200, safe=False)
            else:
                NewsEmail_obj.is_active = False
                NewsEmail_obj.save()
                logger.debug(f'Deactivated NewsEmail subscription for user {request.user.pk}')
                return JsonResponse("Deactivated", status=200, safe=False)
        
        else:
            return redirect('account_login')


###############
# reCAPCHA view
###############

class ReCapcha(View):

    def post(self, request, pk):
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

class LoadProvinces(View):

    def get(self, request):
        provinces = list(Province.objects.all().values('id', 'name', 'offering_count', 'requesting_count').order_by('name'))
        return HttpResponse(json.dumps(provinces), content_type="application/json") 

class LoadMunicipalities(View):

    def get(self, request):
        province_id = request.GET.get('province','') 
        municipalities = list(Municipality.objects.filter(province_id=province_id).values('id', 'name', 'offering_count', 'requesting_count').order_by('name'))
        return HttpResponse(json.dumps(municipalities), content_type="application/json") 

class LoadAreas(View):
    
    def get(self, request):
        municipality_id = request.GET.get('municipality','') 
        areas = list(Area.objects.filter(municipality_id=municipality_id).values('id', 'name', 'offering_count', 'requesting_count').order_by('name'))
        return HttpResponse(json.dumps(areas), content_type="application/json") 
