from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.shortcuts import render
from django.http import HttpResponse

#from dal import autocomplete

from core.forms import AdvertisementForm
from core.models import Advertisement, Municipality, Province, Area

# Create your views here.

def index(request):
    return render(request, 'core/index.html')

# class CityAutocomplete(autocomplete.Select2ListView):
#     def get_list(self):
#         # return all cities name here, it will be auto filtered by super class
#         return ['Pune', 'Patna', 'Mumbai', 'Delhi', ...]
        


class AdListView(ListView):
    model = Advertisement
    context_object_name = 'ads'

class AdCreateView(CreateView):
    model = Advertisement
    form_class = AdvertisementForm
    success_url = reverse_lazy('ad_changelist')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class AdUpdateView(UpdateView):
    model = Advertisement
    form_class = AdvertisementForm
    success_url = reverse_lazy('ad_changelist')

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