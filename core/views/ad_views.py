import json
import json
import locale

from django.http.response import HttpResponseRedirect, JsonResponse
from django.views import generic
from django.views.generic import CreateView, UpdateView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.views import generic
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from django.utils.safestring import mark_safe
from django.forms import HiddenInput, ValidationError
from django.contrib.auth import get_user_model

from lockdown.decorators import lockdown
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Field, HTML, Div
from crispy_forms.bootstrap import InlineRadios, InlineCheckboxes

from core.forms.ad_forms import OfferingDogForm, RequestingDogForm
from core.models import Advertisement, Province, Municipality, Area, DogSizeChoice, NewsEmail
from core.forms.news_email_form import NewsEmailForm
from kontorshund.settings import PRICE_SWISH_EXTEND

User = get_user_model()

locale.setlocale(locale.LC_ALL,'sv_SE.UTF-8')


########
# INDEX 
########

@lockdown()
def index(request):
    return render(request, 'core/index.html')

##########
# PROFILE
# ########

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
                'core/profile/profile.html', 
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
                return render(request, 'core/profile/profile.html', {'form': form})
    else:
        return redirect('account_login')


###########
# LIST ADS
# #########

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

        return render(request, 'core/ads/list_ads.html', context=context)

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


#############
# CREATE ADS
#############

def ChooseAd(request):
    if request.user.is_authenticated:
        return render(request, 'core/ads/choose_ad_type.html')
    else:
        return redirect('account_login')


class NewAdOfferingDog(LoginRequiredMixin, CreateView):
    model = Advertisement
    form_class = OfferingDogForm
    template_name = 'core/ads/new_ad_offering_dog.html'
    success_url = reverse_lazy('profile')
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


class NewAdRequestingDog(CreateView):
    model = Advertisement
    form_class = RequestingDogForm
    success_url = reverse_lazy('ad_changelist')
    template_name = 'core/ads/new_ad_requesting_dog.html'

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

############
# UPDATE ADS
############


class AdUpdateOfferingDogView(UpdateView):
    model = Advertisement
    form_class = OfferingDogForm
    template_name = 'core/ads/update_ad_offering_dog.html'

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


class AdUpdateRequestingDogView(UpdateView):
    model = Advertisement
    form_class = RequestingDogForm
    template_name = 'core/ads/update_ad_requesting_dog.html'


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


#############
# DETAIL VIEW
#############


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


############
# DELETE ADS
############

class DeleteAd(generic.DeleteView):
    model = Advertisement
    template_name = 'core/ads/ad_confirm_delete.html'
    success_url = reverse_lazy('profile')

