from django.urls import path
from core.views import index

from . import views

urlpatterns = [
    path('', index, name='home'),

    # See take and get-ads
    path('ads/take-my-dog', views.AdListTakeMyDog.as_view(), name='view_ads_take_my_dog'),
    path('ads/get-me-a-dog', views.AdListGetMeADog.as_view(), name='view_ads_get_me_a_dog'),

    # Create take and get-ads
    path('add/take-my-dog', views.NewAdTakeMyDog.as_view(), name='new_ad_take_my_dog'),
    path('add/get-me-a-dog', views.NewAdGetMeADog.as_view(), name='new_ad_get_me_a_dog'),

    # Update for take and get-ads
    path('<int:pk>/', views.AdUpdateView.as_view(), name='ad_change'),

    # Path's for area generation
    path('ajax/load-municipalities/', views.load_municipalities, name='ajax_load_municipalities'), 
    path('ajax/load-areas/', views.load_areas, name='ajax_load_areas'), 

    # Autocomplete Breeds URL
    path('breed-autocomplete', views.BreedAutocomplete, name='breed-autocomplete'), 

]
