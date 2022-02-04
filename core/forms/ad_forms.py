from django import forms

from dal import autocomplete

from ..models import Advertisement, Municipality, Area, DogBreed


############
# USER FORMS
############


class OfferingDogForm(forms.ModelForm):
    
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
            'payment_type': 'Välj betalningsmetod, Swish rekommenderas då din annons då dyker upp direkt, bankgiro tar 3-5 arbetsdagar.',
            'hundras': 'Fritextsök - börja skriv och resultat dyker upp',
            'image1': 'Max-storlek 20 MB.',
            'image2': 'Max-storlek 20 MB.',
            'image3': 'Max-storlek 20 MB.',
        }

    def __init__(self, *args, **kwargs):
        super(OfferingDogForm, self).__init__(*args, **kwargs)
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


class RequestingDogForm(forms.ModelForm):
    class Meta:
        model = Advertisement
        fields = ('province', 'municipality', 'area', 'title', 'description', 'days_per_week', 'size_requested', 'image1', 'image2', 'image3', 'payment_type')
        help_texts = {
            'title': 'Skriv en titel som sammanfattar annonsen - T.ex. "Kontor med 10 anställda söker en kontorshund 2 dagar per vecka" eller "Pensionär söker hund 1 dagar per vecka"',
            'description': 'Skriv om dig/er som vill ta hand om en hund, har någon hundvana, vad gör ni om dagarna? osv.',
            'payment_type': 'Välj betalningsmetod, Swish rekommenderas då din annons då dyker upp direkt, bankgiro tar 3-5 arbetsdagar.',
        }



    def __init__(self, *args, **kwargs):
        super(RequestingDogForm, self).__init__(*args, **kwargs)

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
            

########
# ADMIN
########


class AdFormAdmin(forms.ModelForm):
    
    hundras = forms.ModelChoiceField(
        queryset=DogBreed.objects.all(),
        widget=autocomplete.ModelSelect2(url='breed-autocomplete')
    )

    class Meta:
        model = Advertisement
        fields = ('is_published', 'deletion_date', 'is_offering_own_dog', 'is_deleted',  'author', 'province', 'municipality', 'area', 'title', 'name', 'age', 'description', 'days_per_week', 'size_offered', 'size_requested', 'hundras', 'image1', 'image2', 'image3', 'payment_type')


    def __init__(self, *args, **kwargs):
        super(AdFormAdmin, self).__init__(*args, **kwargs)
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


