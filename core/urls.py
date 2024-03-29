from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

from .views import ad_views, payment_views, supporting_views

urlpatterns = [

    path('', ad_views.ListAndSearchAdsView.as_view(), name='list_postings'),
    path('profile', ad_views.Profile.as_view(), name='profile'), 
    path('about', TemplateView.as_view(template_name='about.html'), name='about'),
    path('privacy/', TemplateView.as_view(template_name="core/privacy/terms.html"), name='privacy'),

    path('ads/choose', ad_views.ChooseAd.as_view(), name='choose_ad_type'),
    path('ads/<int:pk>', ad_views.AdDetailView.as_view(), name='ad_detail'),
    path('delete-ad/<int:pk>', ad_views.DeleteAd.as_view(), name='delete_ad'),
    
    path('ads/create/offering-dog', ad_views.NewAdOfferingDog.as_view(), name='new_ad_offering_dog'),
    path('ads/create/requesting-dog', ad_views.NewAdRequestingDog.as_view(), name='new_ad_requesting_dog'),

    path('ads/update/offering-dog/<int:pk>', ad_views.AdUpdateOfferingDogView.as_view(), name='update_ad_offering_dog'),
    path('ads/update/requesting-dog/<int:pk>', ad_views.AdUpdateRequestingDogView.as_view(), name='update_ad_requesting_dog'),

    path('swish/callback', payment_views.SwishCallback.as_view(), name='swish_callback'),
    path('swish-pay/initial/<int:pk>', payment_views.PayForAdSwishTemplate.as_view(), name='swish_payment_initial_template'),
    path('swish-pay/extend/<int:pk>', payment_views.PayForAdSwishTemplate.as_view(), name='swish_payment_extended_template'),
    path('generate-swish-qr-code/<int:pk>', payment_views.GenerateSwishPaymentQrCode.as_view(), name='swish_payment_qr_code'),
    path('generate-swish-request-token/<int:pk>', payment_views.GenerateSwishPaymentRequestToken.as_view(), name='swish_request_token'),
    path('check-initial-payment-status/<int:pk>', payment_views.CheckInitialPaymentStatus.as_view(), name='check_initial_payment_status'),
    path('check-extended-payment-status/<int:pk>', payment_views.CheckExtendedPaymentStatus.as_view(), name='check_extended_payment_status'),
    path('swish-successfull-android', payment_views.AndroidSuccessPage.as_view(), name='android_success_page'),
    path('bg-pay/<int:pk>', payment_views.PayForAdBg.as_view(), name='bg_payment'),
    
    path('handle-email-subscription/<str:uuid>', supporting_views.HandleEmailSubscriptionStatus.as_view(), name='handle_email_subscription_status'), 
    path('deactivate-email-subscription/<str:uuid>', supporting_views.DeactivateEmailSubscription.as_view(), name='deactivate_email_subscription'), 


    path('ajax/load-provinces/', supporting_views.LoadProvinces.as_view(), name='ajax_load_provinces'), 
    path('ajax/load-municipalities/', supporting_views.LoadMunicipalities.as_view(), name='ajax_load_municipalities'), 
    path('ajax/load-areas/', supporting_views.LoadAreas.as_view(), name='ajax_load_areas'), 

    path('recapcha/<int:pk>', supporting_views.ReCapcha.as_view(), name='recapcha'),
    path('breed-autocomplete', supporting_views.BreedAutocomplete.as_view(), name='breed-autocomplete'), 
]

if bool(settings.DEBUG):
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
