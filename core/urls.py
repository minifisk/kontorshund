from django.urls import path
from django.conf import settings
from django.conf.urls.static import static


from . import views

urlpatterns = [
    path('', views.testindex, name='home'),

    path('testindex', views.index, name='home'), 

    # See take and get-ads
    path('ads/take-my-dog', views.AdListTakeMyDog.as_view(), name='view_ads_take_my_dog'),
    path('ads/get-me-a-dog', views.AdListGetMeADog.as_view(), name='view_ads_get_me_a_dog'),

    # View of a specific ad
    path('ads/<int:pk>', views.AdDetailView.as_view(), name='ad-detail'),

    # Pay for an ad
    path('swish-pay/<int:pk>', views.PayForAdSwishTemplate, name='swish_payment_template'),
    path('generate-swish-qr-code/<int:pk>', views.GenerateSwishPaymentQrCode, name='swish_payment_qr_code'),
    path('generate-swish-request-token/<int:pk>', views.GenerateSwishPaymentRequestToken, name='swish_request_token'),
    path('check-payment-status/<int:pk>', views.check_payment_status, name='swish_payment_status'),
    path('bg-pay/<int:pk>', views.PayForAdBG, name='bg_payment'),

    
    # Create take and get-ads
    path('add/take-my-dog', views.NewAdTakeMyDog.as_view(), name='new_ad_take_my_dog'),
    path('add/get-me-a-dog', views.NewAdGetMeADog.as_view(), name='new_ad_get_me_a_dog'),

    # Update for take and get-ads
    path('<int:pk>/', views.AdUpdateView.as_view(), name='ad_change'),


    # Path's for area generation
    path('ajax/load-municipalities/', views.load_municipalities, name='ajax_load_municipalities'), 
    path('ajax/load-areas/', views.load_areas, name='ajax_load_areas'), 

    # Autocomplete Breeds URL
    path('breed-autocomplete', views.BreedAutocomplete.as_view(), name='breed-autocomplete'), 

    #path("upload", views.image_upload, name="upload"),

    # Swish callback
    path('swish/callback', views.swish_callback, name='swish_callback'),


]

if bool(settings.DEBUG):
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
