from django.urls import path
from accounts.views import home_page_view

urlpatterns = [
    path('hej', home_page_view, name='home'),
]
