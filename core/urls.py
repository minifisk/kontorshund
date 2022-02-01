from django.urls import path
from django.conf import settings
from django.conf.urls.static import static


from . import views

urlpatterns = [
    
    path('', views.index, name='index'), 
    path('profile', views.profile, name='profile'), 

    path('deactivate-email-subscription/<str:uuid>', views.deactivate_news_email_subscription, name='deactivate_email_subscription'),
    path('handle-email-subscription/<str:uuid>', views.handle_email_subscription_status, name='handle_email_subscription_status'), 

    path('ads/choose', views.ChooseAd, name='choose_ad_type'),
    path('ads/list', views.ListAndSearchAdsView, name='list_ads'),
    path('ads/<int:pk>', views.AdDetailView.as_view(), name='ad_detail'),
    path('delete-ad/<int:pk>', views.DeleteAd.as_view(), name='delete_ad'),
    
    path('ads/create/take-my-dog', views.NewAdOfferingDog.as_view(), name='new_ad_take_my_dog'),
    path('ads/create/get-me-a-dog', views.NewAdRequestingDog.as_view(), name='new_ad_get_me_a_dog'),

    path('ads/update/take-my-dog/<int:pk>', views.AdUpdateOfferingDogView.as_view(), name='ad_update_take'),
    path('ads/update/get-me-a-dog/<int:pk>', views.AdUpdateRequestingDogView.as_view(), name='ad_update_get'),
    
    path('recapcha/<int:pk>', views.recapcha, name='recapcha'),

    path('swish/callback', views.swish_callback, name='swish_callback'),
    path('swish-pay/initial/<int:pk>', views.PayForAdSwishTemplate, name='swish_payment_initial_template'),
    path('swish-pay/extend/<int:pk>', views.PayForAdSwishTemplate, name='swish_payment_extended_template'),
    path('generate-swish-qr-code/<int:pk>', views.GenerateSwishPaymentQrCode, name='swish_payment_qr_code'),
    path('generate-swish-request-token/<int:pk>', views.GenerateSwishPaymentRequestToken, name='swish_request_token'),
    path('check-initial-payment-status/<int:pk>', views.check_initial_payment_status, name='check_initial_payment_status'),
    path('check-extended-payment-status/<int:pk>', views.check_extended_payment_status, name='check_extended_payment_status'),
    path('swish-successfull-android', views.android_success_page, name='android_success_page'),
    path('bg-pay/<int:pk>', views.PayForAdBG, name='bg_payment'),

    path('ajax/load-provinces/', views.load_provinces, name='ajax_load_provinces'), 
    path('ajax/load-municipalities/', views.load_municipalities, name='ajax_load_municipalities'), 
    path('ajax/load-areas/', views.load_areas, name='ajax_load_areas'), 

    path('breed-autocomplete', views.BreedAutocomplete.as_view(), name='breed-autocomplete'), 
]

if bool(settings.DEBUG):
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
