from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.shortcuts import render
from django.http import HttpResponse

from core.forms import AdvertisementForm

from core.models import Advertisement, Municipality, Province

# Create your views here.

def index(request):

    return render(request, 'core/index.html')


class AdListView(ListView):
    model = Advertisement
    context_object_name = 'ads'

class AdCreateView(CreateView):
    model = Advertisement
    form_class = AdvertisementForm
    success_url = reverse_lazy('ad_changelist')

class AdUpdateView(UpdateView):
    model = Advertisement
    form_class = AdvertisementForm
    success_url = reverse_lazy('ad_changelist')

# View to be used for getting Municipalities connected to a Province
def load_municipalities(request):
    province_id = request.GET.get('province')
    municipalities = Municipality.objects.filter(province_id=province_id).order_by('name')
    return render(request, 'municipality_dropdown_list_options.html', {'municipalities': municipalities})