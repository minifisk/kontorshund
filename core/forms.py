from django import forms
from django.conf import settings
from django.core.validators import RegexValidator
from django.db.models import query


from kontorshund.settings import PRICE_BANKGIRO
from kontorshund.settings import PRICE_SWISH


from .models import Advertisement, DogSizeChoices, Municipality, Area, DogBreeds

from dal import autocomplete



class NewAdTakeMyDogForm(forms.ModelForm):
    
    hundras = forms.ModelChoiceField(
        queryset=DogBreeds.objects.all(),
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

        }

    def __init__(self, *args, **kwargs):
        super(NewAdTakeMyDogForm, self).__init__(*args, **kwargs)
        self.fields['municipality'].queryset = Municipality.objects.none()
        self.fields['area'].queryset = Area.objects.none()
        self.fields['area'].required = False
        self.fields['image2'].required = False
        self.fields['image3'].required = False
        self.fields['size_offered'].empty_label = None
        
        # for field in self.fields.values():
        #     field.error_messages = {'required':'Fältet {fieldname} är obligatoriskt'.format(
        #         fieldname=field.label)}


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


class NewAdFormAdmin(forms.ModelForm):
    
    hundras = forms.ModelChoiceField(
        queryset=DogBreeds.objects.all(),
        widget=autocomplete.ModelSelect2(url='breed-autocomplete')
    )

    class Meta:
        model = Advertisement
        fields = ('is_published', 'is_offering_own_dog', 'author', 'province', 'municipality', 'area', 'title', 'name', 'age', 'description', 'days_per_week', 'size_offered', 'size_requested', 'hundras', 'image1', 'image2', 'image3', 'payment_type')


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
        
        for field in self.fields.values():
            field.error_messages = {'required':'Fältet {fieldname} är obligatoriskt'.format(
                fieldname=field.label)}

class NewAdGetMeADogForm(forms.ModelForm):
    class Meta:
        model = Advertisement
        fields = ('province', 'municipality', 'area', 'title', 'description', 'days_per_week', 'size_requested', 'image1', 'image2', 'image3', 'payment_type')
        help_texts = {
            'title': 'Skriv en titel som sammanfattar annonsen - T.ex. "Kontor med 10 anställda söker en kontorshund 2 dagar per vecka" eller "Pensionär söker hund 1 dagar per vecka"',
            'description': 'Skriv om dig/er som vill ta hand om en hund, har någon hundvana, vad gör ni om dagarna? osv.',
            'payment_type': 'Välj betalningsmetod, Swish rekommenderas då din annons då dyker upp direkt.',

        }



    def __init__(self, *args, **kwargs):
        super(NewAdGetMeADogForm, self).__init__(*args, **kwargs)
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
                

            except (ValueError, TypeError):
                pass # invalid input from the client; ignore and fallback to empty Municipality/Area queryset
            
            for field in self.fields.values():
                field.error_messages = {'required':'Fältet {fieldname} är obligatoriskt'.format(
                fieldname=field.label)}

phone_number_validator = RegexValidator(r"^(07[0236])\s*(\d{4})\s*(\d{3})$", "Telefonnummer skall anges i formatet 0723456789 (utan mellanslag)")

class PhoneNumberForm(forms.Form):
    phone_number = forms.CharField(
        required=True,
        label='Ditt telefonnummer', 
        validators=[phone_number_validator], 
        widget=forms.TextInput(attrs={'placeholder': '0701234567'})
    )


