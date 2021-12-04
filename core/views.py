from django.views import generic
from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic

#from dal import autocomplete

from core.forms import NewAdTakeMyDogForm, NewAdGetMeADogForm
from core.models import Advertisement, Municipality, Area, DogBreeds


from dal import autocomplete


# Create your views here.

def index(request):
    return render(request, 'core/index.html')

class BreedAutocomplete(autocomplete.Select2QuerySetView):

    def get_queryset(self):

        if not self.request.user.is_authenticated:
            return DogBreeds.objects.none()

        qs = DogBreeds.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

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
    success_url = reverse_lazy('view_ads_take_my_dog')
    template_name = 'core/advertisement_form_take.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.is_offering_own_dog = True
        return super().form_valid(form)


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