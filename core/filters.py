import django_filters 
from core.models import Advertisement, DAYS_PER_WEEK_CHOICES, DogSizeChoice
from django import forms


class AdOfferingDogFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains')
    days_per_week = django_filters.MultipleChoiceFilter(choices=DAYS_PER_WEEK_CHOICES, widget=forms.CheckboxSelectMultiple)
    size_offered = django_filters.ModelMultipleChoiceFilter(queryset=DogSizeChoice.objects.all(), widget=forms.CheckboxSelectMultiple)

    


    class Meta:
        model =  Advertisement
        fields = ('province', 'municipality', 'area', 'hundras', 'title', 'days_per_week', 'size_offered')