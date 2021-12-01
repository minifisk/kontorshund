from django import forms
from .models import Advertisement, Municipality, Area

class AdvertisementForm(forms.ModelForm):
    class Meta:
        model = Advertisement
        fields = ('province', 'municipality', 'area', 'title', 'description', 'days_per_week', 'breed', 'size')

    def __init__(self, *args, **kwargs):
        super(AdvertisementForm, self).__init__(*args, **kwargs)
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
            

