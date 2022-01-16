import django_filters 
from core.models import Advertisement, DAYS_PER_WEEK_CHOICES, DogSizeChoice, Area, Municipality
from django import forms


class AdOfferingDogFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains')
    days_per_week = django_filters.MultipleChoiceFilter(choices=DAYS_PER_WEEK_CHOICES, widget=forms.CheckboxSelectMultiple)
    size_offered = django_filters.ModelMultipleChoiceFilter(queryset=DogSizeChoice.objects.all(), widget=forms.CheckboxSelectMultiple)


    class Meta:
        model =  Advertisement
        fields = ('province', 'municipality', 'area', 'hundras', 'title', 'days_per_week', 'size_offered')

    def __init__(self, *args, **kwargs):
        super(AdOfferingDogFilter, self).__init__(*args, **kwargs)

        from pprint import pprint
        pprint(vars(self))

        # if (self.instance):
        #     if (not self.instance.area):
        #         self.fields['area'].queryset = Area.objects.none()
        # else:
        #     self.fields['municipality'].queryset = Municipality.objects.none()
        #     self.fields['area'].queryset = Area.objects.none()
        #     self.fields['area'].required = False

        # if 'province' in self.data:
        #     try:
        #         # Set municipality queryset
        #         province_id = int(self.data.get('province'))
        #         self.fields['municipality'].queryset = Municipality.objects.filter(province_id=province_id).order_by('name')
            
        #         # Set area queryset
        #         municipality_id = int(self.data.get('municipality'))
        #         self.fields['area'].queryset = Area.objects.filter(municipality_id=municipality_id).order_by('name')
                

        #     except (ValueError, TypeError):
        #         pass # invalid input from the client; ignore and fallback to empty Municipality/Area queryset
            
            # for field in self.fields.values():
            #     field.error_messages = {'required':'Fältet {fieldname} är obligatoriskt'.format(
            #     fieldname=field.label)}