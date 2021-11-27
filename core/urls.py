from django.urls import path
from core.views import index

from . import views

urlpatterns = [
    path('', index, name='home'),
    path('ads/', views.AdListView.as_view(), name='ad_changelist'),
    path('add/', views.AdCreateView.as_view(), name='ad_add'),
    path('<int:pk>/', views.AdUpdateView.as_view(), name='ad_change'),
]
