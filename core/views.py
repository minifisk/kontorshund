from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.shortcuts import render
from django.http import HttpResponse

from core.forms import AdvertisementForm

from core.models import Advertisement

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