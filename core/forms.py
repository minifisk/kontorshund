from django import forms
from django.conf import settings
from django.core.validators import RegexValidator


from kontorshund.settings import PRICE_BANKGIRO
from kontorshund.settings import PRICE_SWISH


from .models import Advertisement, Municipality, Area, DogBreeds

from dal import autocomplete




class NewAdTakeMyDogForm(forms.ModelForm):
    
    hundras = forms.ModelChoiceField(
        queryset=DogBreeds.objects.all(),
        widget=autocomplete.ModelSelect2(url='breed-autocomplete')
    )

    class Meta:
        model = Advertisement
        fields = ('province', 'municipality', 'area', 'title', 'name', 'age', 'description', 'days_per_week', 'size_offered', 'hundras', 'image1', 'image2', 'image3', 'payment_type')


    def __init__(self, *args, **kwargs):
        super(NewAdTakeMyDogForm, self).__init__(*args, **kwargs)
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
            


class NewAdTakeMyDogFormAdmin(forms.ModelForm):
    
    hundras = forms.ModelChoiceField(
        queryset=DogBreeds.objects.all(),
        widget=autocomplete.ModelSelect2(url='breed-autocomplete')
    )

    class Meta:
        model = Advertisement
        fields = ('author', 'province', 'municipality', 'area', 'title', 'name', 'age', 'description', 'days_per_week', 'size_offered', 'hundras', 'image1', 'image2', 'image3', 'payment_type')


    def __init__(self, *args, **kwargs):
        super(NewAdTakeMyDogFormAdmin, self).__init__(*args, **kwargs)
        print(self.instance)

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
            

class NewAdGetMeADogForm(forms.ModelForm):
    class Meta:
        model = Advertisement
        fields = ('province', 'municipality', 'area', 'title', 'description', 'days_per_week', 'size_requested', 'image1', 'image2', 'image3', 'payment_type')
        help_texts = {
            'size_requested': 'Håll in cmd (mac) eller ctrl (windows) för att markera flera',
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
            
phone_number_validator = RegexValidator(r"^(07[0236])\s*(\d{4})\s*(\d{3})$", "Telefonnummer skall anges i formatet 0723456789 (utan mellanslag)")

class PhoneNumberForm(forms.Form):
    phone_number = forms.CharField(
        required=True,
        label='Ditt telefonnummer', 
        validators=[phone_number_validator], 
        widget=forms.TextInput(attrs={'placeholder': '0701234567'})
    )


