from django.urls import path
from django.conf import settings
from django.conf.urls.static import static


from .views import ad_views, payment_views, supporting_views

urlpatterns = [
    
    path('', ad_views.index, name='index'), 
    path('profile', ad_views.profile, name='profile'), 

    path('deactivate-email-subscription/<str:uuid>', supporting_views.deactivate_news_email_subscription, name='deactivate_email_subscription'),
    path('handle-email-subscription/<str:uuid>', supporting_views.handle_email_subscription_status, name='handle_email_subscription_status'), 

    path('ads/choose', ad_views.ChooseAd, name='choose_ad_type'),
    path('ads/list', ad_views.ListAndSearchAdsView, name='list_ads'),
    path('ads/<int:pk>', ad_views.AdDetailView.as_view(), name='ad_detail'),
    path('delete-ad/<int:pk>', ad_views.DeleteAd.as_view(), name='delete_ad'),
    
    path('ads/create/take-my-dog', ad_views.NewAdOfferingDog.as_view(), name='new_ad_take_my_dog'),
    path('ads/create/get-me-a-dog', ad_views.NewAdRequestingDog.as_view(), name='new_ad_get_me_a_dog'),

    path('ads/update/take-my-dog/<int:pk>', ad_views.AdUpdateOfferingDogView.as_view(), name='ad_update_take'),
    path('ads/update/get-me-a-dog/<int:pk>', ad_views.AdUpdateRequestingDogView.as_view(), name='ad_update_get'),
    
    path('recapcha/<int:pk>', supporting_views.recapcha, name='recapcha'),

    path('swish/callback', payment_views.swish_callback, name='swish_callback'),
    path('swish-pay/initial/<int:pk>', payment_views.PayForAdSwishTemplate, name='swish_payment_initial_template'),
    path('swish-pay/extend/<int:pk>', payment_views.PayForAdSwishTemplate, name='swish_payment_extended_template'),
    path('generate-swish-qr-code/<int:pk>', payment_views.GenerateSwishPaymentQrCode, name='swish_payment_qr_code'),
    path('generate-swish-request-token/<int:pk>', payment_views.GenerateSwishPaymentRequestToken, name='swish_request_token'),
    path('check-initial-payment-status/<int:pk>', payment_views.check_initial_payment_status, name='check_initial_payment_status'),
    path('check-extended-payment-status/<int:pk>', payment_views.check_extended_payment_status, name='check_extended_payment_status'),
    path('swish-successfull-android', payment_views.android_success_page, name='android_success_page'),
    path('bg-pay/<int:pk>', payment_views.PayForAdBG, name='bg_payment'),

    path('ajax/load-provinces/', supporting_views.load_provinces, name='ajax_load_provinces'), 
    path('ajax/load-municipalities/', supporting_views.load_municipalities, name='ajax_load_municipalities'), 
    path('ajax/load-areas/', supporting_views.load_areas, name='ajax_load_areas'), 

    path('breed-autocomplete', supporting_views.BreedAutocomplete.as_view(), name='breed-autocomplete'), 
]

if bool(settings.DEBUG):
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
