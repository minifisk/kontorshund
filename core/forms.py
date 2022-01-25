from django import forms
from django.conf import settings
from django.core.validators import RegexValidator
from django.db.models import query
from django.forms.models import ModelChoiceField


from kontorshund.settings import PRICE_BANKGIRO_INITIAL
from kontorshund.settings import PRICE_SWISH_INITIAL


from .models import DAYS_PER_WEEK_CHOICES, Advertisement, DogSizeChoice, Municipality, Area, DogBreed, NewsEmail

from dal import autocomplete
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Field, Row, Column, HTML, Div
from crispy_forms.bootstrap import (
    PrependedText, PrependedAppendedText, FormActions, InlineRadios, InlineCheckboxes)

    

######################
# SEARCH FOR AD FORMS
#####################

class SearchAllAdsForm(forms.ModelForm):
    days_per_week = forms.MultipleChoiceField(choices=DAYS_PER_WEEK_CHOICES, widget=forms.CheckboxSelectMultiple(), label='Dagar per vecka')

    class Meta:
        model = Advertisement
        fields = ('province', 'municipality', 'area', 'days_per_week')

    def __init__(self, *args, **kwargs):
        super(SearchAllAdsForm, self).__init__(*args, **kwargs)
        self.fields['days_per_week'].required = False
        self.fields['province'].required = False
        self.fields['municipality'].required = False
        self.fields['area'].required = False
        self.fields['municipality'].queryset = Municipality.objects.none()
        self.fields['area'].queryset = Area.objects.none()
        self.fields['days_per_week'].required = False
    

        if 'province' in self.data:
            try:
                # Set municipality queryset
                province_id = int(self.data.get('province'))
                self.fields['municipality'].queryset = Municipality.objects.filter(province_id=province_id).order_by('name')
            
                # Set area queryset
                municipality_id = int(self.data.get('municipality'))
                self.fields['area'].queryset = Area.objects.filter(municipality_id=municipality_id).order_by('name')
                
            except (ValueError, TypeError) as e:
                pass # invalid input from the client; ignore and fallback to empty Municipality/Area queryset


class SearchOfferingDogAdsForm(forms.ModelForm):
    days_per_week = forms.MultipleChoiceField(choices=DAYS_PER_WEEK_CHOICES, widget=forms.CheckboxSelectMultiple(), label='Dagar per vecka')
    size_offered = forms.ModelMultipleChoiceField(queryset=DogSizeChoice.objects.all(), widget=forms.CheckboxSelectMultiple(), label='Hundstorlek')

    class Meta:
        model = Advertisement
        fields = ('province', 'municipality', 'area', 'days_per_week', 'size_offered', 'hundras')

    def __init__(self, *args, **kwargs):
        super(SearchOfferingDogAdsForm, self).__init__(*args, **kwargs)
        self.fields['size_offered'].required = False
        self.fields['days_per_week'].required = False
        self.fields['province'].required = False
        self.fields['municipality'].required = False
        self.fields['area'].required = False
        self.fields['hundras'].required = False

        self.fields['municipality'].queryset = Municipality.objects.none()
        self.fields['area'].queryset = Area.objects.none()
    

        if 'province' in self.data:
            try:
                # Set municipality queryset
                province_id = int(self.data.get('province'))
                self.fields['municipality'].queryset = Municipality.objects.filter(province_id=province_id).order_by('name')
            
                # Set area queryset
                municipality_id = int(self.data.get('municipality'))
                self.fields['area'].queryset = Area.objects.filter(municipality_id=municipality_id).order_by('name')
                
            except (ValueError, TypeError) as e:
                pass # invalid input from the client; ignore and fallback to empty Municipality/Area queryset



class SearchRequestingDogAdsForm(forms.ModelForm):
    days_per_week = forms.MultipleChoiceField(choices=DAYS_PER_WEEK_CHOICES, widget=forms.CheckboxSelectMultiple(), label='Dagar per vecka (flerval)')
    size_requested = forms.ModelMultipleChoiceField(queryset=DogSizeChoice.objects.all(), widget=forms.CheckboxSelectMultiple(), label='Hundstorlek')


    class Meta:
        model = Advertisement
        fields = ('province', 'municipality', 'area', 'days_per_week', 'size_requested')


    def __init__(self, *args, **kwargs):
        super(SearchRequestingDogAdsForm, self).__init__(*args, **kwargs)

        self.fields['size_requested'].required = False
        self.fields['days_per_week'].required = False
        self.fields['province'].required = False
        self.fields['municipality'].required = False
        self.fields['area'].required = False

        self.fields['municipality'].queryset = Municipality.objects.none()
        self.fields['area'].queryset = Area.objects.none()

        if 'province' in self.data:
            try:
                # Set municipality queryset
                province_id = int(self.data.get('province'))
                self.fields['municipality'].queryset = Municipality.objects.filter(province_id=province_id).order_by('name')
            
                # Set area queryset
                municipality_id = int(self.data.get('municipality'))
                self.fields['area'].queryset = Area.objects.filter(municipality_id=municipality_id).order_by('name')
                

            except (ValueError, TypeError):
                pass # invalid input from the client; ignore and fallback to empty Municipality/Area queryset
            


#################
# CREATE AD FORMS
#################


class NewAdTakeMyDogForm(forms.ModelForm):
    
    hundras = forms.ModelChoiceField(
        queryset=DogBreed.objects.all(),
        widget=autocomplete.ModelSelect2(url='breed-autocomplete')
    )

    image1 = forms.ImageField(label='')
    image2 = forms.ImageField(label='')
    image3 = forms.ImageField(label='')


    class Meta:
        model = Advertisement
        fields = ('province', 'municipality', 'area', 'title', 'name', 'age', 'description', 'days_per_week', 'size_offered', 'hundras', 'image1', 'image2', 'image3', 'payment_type')
        help_texts = {
            'title': 'Skriv en titel som sammanfattar annonsen - T.ex. "Frans, Border Collie, Söker kompis för 3 dagar per vecka"',
            'description': 'Skriv kort om hunden och er som har hunden, vad har hunden för typ av personlighet? Finns det saker den gillar mer eller mindre? Inom vilket område kan ni tänka er att länmna/hämta hunden?',
            'payment_type': 'Välj betalningsmetod, Swish rekommenderas då din annons då dyker upp direkt.',
            'hundras': 'Fritextsök - börja skriv och resultat dyker upp',
            'image1': 'Max-storlek 20 MB.',
            'image2': 'Max-storlek 20 MB.',
            'image3': 'Max-storlek 20 MB.',
        }

    def __init__(self, *args, **kwargs):
        super(NewAdTakeMyDogForm, self).__init__(*args, **kwargs)
        self.fields['image2'].required = False
        self.fields['image3'].required = False
        self.fields['size_offered'].empty_label = None
        

        # If user is creating new ad, not editing
        if self.instance.id == None:
            self.fields['municipality'].queryset = Municipality.objects.none()
            self.fields['area'].queryset = Area.objects.none()

        # If user is editing existing ad
        else: 
            # If province selected, update municipality queryset
            if self.instance.province:
                self.fields['municipality'].queryset = Municipality.objects.filter(province_id=self.instance.province.pk).order_by('name')
            
            # If municipality selected, update area queryset
            if self.instance.municipality:
                self.fields['area'].queryset = Area.objects.filter(municipality_id=self.instance.municipality.pk).order_by('name')

        

        if 'province' in self.data:
            try:
                # Set municipality queryset
                province_id = int(self.data.get('province'))
                self.fields['municipality'].queryset = Municipality.objects.filter(province_id=province_id).order_by('name')
            
                # Set area queryset
                municipality_id = int(self.data.get('municipality'))
                self.fields['area'].queryset = Area.objects.filter(municipality_id=municipality_id).order_by('name')
                
            except (ValueError, TypeError) as e:
                pass # invalid input from the client; ignore and fallback to empty Municipality/Area queryset


class NewAdGetMeADogForm(forms.ModelForm):
    class Meta:
        model = Advertisement
        fields = ('province', 'municipality', 'area', 'title', 'description', 'days_per_week', 'size_requested', 'image1', 'image2', 'image3', 'payment_type')
        help_texts = {
            'title': 'Skriv en titel som sammanfattar annonsen - T.ex. "Kontor med 10 anställda söker en kontorshund 2 dagar per vecka" eller "Pensionär söker hund 1 dagar per vecka"',
            'description': 'Skriv om dig/er som vill ta hand om en hund, har någon hundvana, vad gör ni om dagarna? osv.',
            'payment_type': 'Välj betalningsmetod, Swish rekommenderas då din annons då dyker upp direkt.',
            'image1': 'Max-storlek 20 MB.',
            'image2': 'Max-storlek 20 MB.',
            'image3': 'Max-storlek 20 MB.',
        }



    def __init__(self, *args, **kwargs):
        super(NewAdGetMeADogForm, self).__init__(*args, **kwargs)

        # If user is creating new ad, not editing
        if self.instance.id == None:
            self.fields['municipality'].queryset = Municipality.objects.none()
            self.fields['area'].queryset = Area.objects.none()

        # If user is editing existing ad
        else: 
            # If province selected, update municipality queryset
            if self.instance.province:
                self.fields['municipality'].queryset = Municipality.objects.filter(province_id=self.instance.province.pk).order_by('name')
            
            # If municipality selected, update area queryset
            if self.instance.municipality:
                self.fields['area'].queryset = Area.objects.filter(municipality_id=self.instance.municipality.pk).order_by('name')

        if 'province' in self.data:
            try:
                # Set municipality queryset
                province_id = int(self.data.get('province'))
                self.fields['municipality'].queryset = Municipality.objects.filter(province_id=province_id).order_by('name')
            
                # Set area queryset
                municipality_id = int(self.data.get('municipality'))
                self.fields['area'].queryset = Area.objects.filter(municipality_id=municipality_id).order_by('name')
                

            except (ValueError, TypeError):
                pass # invalid input from the client; ignore and fallback to empty Municipality/Area queryset
            

##########################
# CREATE AD FORMS - ADMIN
##########################


class NewAdFormAdmin(forms.ModelForm):
    
    hundras = forms.ModelChoiceField(
        queryset=DogBreed.objects.all(),
        widget=autocomplete.ModelSelect2(url='breed-autocomplete')
    )

    class Meta:
        model = Advertisement
        fields = ('is_published', 'is_offering_own_dog', 'is_deleted', 'deletion_date', 'author', 'province', 'municipality', 'area', 'title', 'name', 'age', 'description', 'days_per_week', 'size_offered', 'size_requested', 'hundras', 'image1', 'image2', 'image3', 'payment_type')


    def __init__(self, *args, **kwargs):
        super(NewAdFormAdmin, self).__init__(*args, **kwargs)
        self.fields['name'].required = False
        self.fields['size_requested'].required = False
        self.fields['size_offered'].required = False
        self.fields['hundras'].required = False

        if (self.instance):
            if (not self.instance.area):
                self.fields['area'].queryset = Area.objects.none()
        else:
            self.fields['municipality'].queryset = Municipality.objects.none()
            self.fields['area'].queryset = Area.objects.none()
            self.fields['area'].required = False

        if 'province' in self.data:
            try:
                # Set municipality queryset
                province_id = int(self.data.get('province'))
                self.fields['municipality'].queryset = Municipality.objects.filter(province_id=province_id).order_by('name')
            
                # Set area queryset
                municipality_id = int(self.data.get('municipality'))
                self.fields['area'].queryset = Area.objects.filter(municipality_id=municipality_id).order_by('name')
                
            except (ValueError, TypeError) as e:
                pass # invalid input from the client; ignore and fallback to empty Municipality/Area queryset
        
        # for field in self.fields.values():
        #     field.error_messages = {'required':'Fältet {fieldname} är obligatoriskt'.format(
        #         fieldname=field.label)}







##################
# NEWS EMAIL FORM
##################

class NewsEmailForm(forms.ModelForm):

    class Meta:
        model = NewsEmail 
        fields = ('province', 'municipality', 'areas', 'interval', 'ad_type')
        help_texts = {
            'areas': 'Håll in cmd (mac) eller ctrl (windows) för att markera flera',
            'interval': 'Hur ofta du vill få ett mail med nya annonser i valt område.',
            'ad_type': 'Vilka typer av annonser du vill bevaka.',

        }

    def __init__(self, *args, **kwargs):
        super(NewsEmailForm, self).__init__(*args, **kwargs)
        self.fields['province'].required = True
        self.fields['municipality'].required = True
        self.fields['areas'].required = False
        self.fields['interval'].required = True
        self.fields['ad_type'].required = True
        self.fields["interval"].choices = list(self.fields["interval"].choices)[1:] 
        self.fields["ad_type"].choices = list(self.fields["ad_type"].choices)[1:] 
        self.helper = FormHelper()
        if self.instance.is_active:
            button_text = 'Inaktivera'
            button_type = 'danger'
        else:
            button_text = 'Aktivera'
            button_type = 'success'

        self.helper.layout = Layout(
            Row(
                Column('province', css_class='form-group col-2 mb-0'),
                Column('municipality', css_class='form-group col-2 mb-0 ml-4'),
                Column('areas', css_class='form-group col-3 mb-0 ml-4'),
                Column(
                    InlineRadios('interval'), 
                    css_class='form-group col-1 mb-0 ml-4'
                ),
                Column(
                    InlineRadios('ad_type', css_class='p-7'), 
                    css_class='form-group col-1 mb-0 ml-4'
                ),
                Column(
                    FormActions(
                        Submit('submit', 'Spara bevakning', css_class='btn btn-sm btn-primary'),                            
                        HTML(f'<button id="cancel-subscription-button" class="mt-2 btn btn-sm btn-{button_type}">{button_text}</button>')
                    ), 
                    css_class='form-group col-1 mt-4 mb-0 ml-4'
                ),
                
            ),
        )

        # If no province selected, clear other fields
        if not self.instance.province:
            self.fields['municipality'].queryset = Municipality.objects.none()
            self.fields['areas'].queryset = Area.objects.none()
        
        # If province selected, update municipality queryset
        if self.instance.province:
            self.fields['municipality'].queryset = Municipality.objects.filter(province_id=self.instance.province.pk).order_by('name')
        
        # If municipality selected, update area queryset
        if self.instance.municipality:
            self.fields['areas'].queryset = Area.objects.filter(municipality_id=self.instance.municipality.pk).order_by('name')


        if 'province' in self.data:
            try:
                # Set municipality queryset
                province_id = int(self.data.get('province'))
                self.fields['municipality'].queryset = Municipality.objects.filter(province_id=province_id).order_by('name')
            
                # Set area queryset
                municipality_id = int(self.data.get('municipality'))
                self.fields['areas'].queryset = Area.objects.filter(municipality_id=municipality_id).order_by('name')
                
            except (ValueError, TypeError) as e:
                pass # invalid input from the client; ignore and fallback to empty Municipality/Area queryset

##########################
# NEWS EMAIL FORM - ADMIN
##########################

class NewsEmailFormAdmin(forms.ModelForm):

    TRUE_FALSE_CHOICES = (
    (True, 'True'),
    (False, 'False')
    )

    is_active = forms.ChoiceField(choices = TRUE_FALSE_CHOICES, label="Is active", 
                              initial='', widget=forms.Select(), required=True)


    class Meta:
        model = NewsEmail 
        fields = ('ad_type', 'user', 'province', 'municipality', 'areas', 'interval')

    def __init__(self, *args, **kwargs):
        super(NewsEmailFormAdmin, self).__init__(*args, **kwargs)
        
        if not self.instance.province:
            self.fields['municipality'].queryset = Municipality.objects.none()
            self.fields['areas'].queryset = Area.objects.none()
        self.fields['areas'].required = False

        # If no province selected, clear other fields
        if not self.instance.province:
            self.fields['municipality'].queryset = Municipality.objects.none()
            self.fields['areas'].queryset = Area.objects.none()
        
        # If province selected, update municipality queryset
        if self.instance.province:
            self.fields['municipality'].queryset = Municipality.objects.filter(province_id=self.instance.province.pk).order_by('name')
        
        # If municipality selected, update area queryset
        if self.instance.municipality:
            self.fields['areas'].queryset = Area.objects.filter(municipality_id=self.instance.municipality.pk).order_by('name')


        if 'province' in self.data:
            try:
                # Set municipality queryset
                province_id = int(self.data.get('province'))
                self.fields['municipality'].queryset = Municipality.objects.filter(province_id=province_id).order_by('name')
            
                # Set area queryset
                municipality_id = int(self.data.get('municipality'))
                self.fields['areas'].queryset = Area.objects.filter(municipality_id=municipality_id).order_by('name')
                
            except (ValueError, TypeError) as e:
                pass # invalid input from the client; ignore and fallback to empty Municipality/Area queryset






