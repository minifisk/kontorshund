from django import forms
from .models import Advertisement, Province, Municipality

class AdvertisementForm(forms.ModelForm):
    class Meta:
        model = Advertisement
        fields = ('author', 'province', 'municipality', 'title', 'description', 'days_per_week', 'breed', 'size')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['municipality'].queryset = Municipality.objects.none()