from django.urls import path
from accounts.views import UserDeactivateView

urlpatterns = [
        path('close-account', UserDeactivateView.as_view(), name='deactivate_account'), 
]
