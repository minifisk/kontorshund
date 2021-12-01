from django.urls import path
from core.views import index

from . import views

urlpatterns = [
    path('', index, name='home'),
    path('ads/', views.AdListView.as_view(), name='ad_changelist'),
    path('add/take-my-dog', views.NewAdTakeMyDog.as_view(), name='new_ad_take_my_dog'),
    path('add/get-me-a-dog', views.NewAdGetMeADog.as_view(), name='new_ad_get_me_a_dog'),
    path('<int:pk>/', views.AdUpdateView.as_view(), name='ad_change'),

    path('ajax/load-municipalities/', views.load_municipalities, name='ajax_load_municipalities'), 
    path('ajax/load-areas/', views.load_areas, name='ajax_load_areas'), 
]
