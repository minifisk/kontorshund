from django.contrib import admin
from django.contrib.sites.models import Site

from core.models import Payment, Province, Municipality, Advertisement, Area, DogSizeChoices, DogBreeds
from core.forms import NewAdTakeMyDogForm, NewAdTakeMyDogFormAdmin

# Register your models here.

class ProvinceAdmin(admin.ModelAdmin):
    model = Province

admin.site.register(Province, ProvinceAdmin)


class MunicipalityAdmin(admin.ModelAdmin):
    model = Municipality

admin.site.register(Municipality, MunicipalityAdmin)

class AreaAdmin(admin.ModelAdmin):
    model = Area

admin.site.register(Area, AreaAdmin)


class DogSizeAdmin(admin.ModelAdmin):
    model = DogSizeChoices

admin.site.register(DogSizeChoices, DogSizeAdmin)


class DogBreedsAdmin(admin.ModelAdmin):
    model = DogBreeds

admin.site.register(DogBreeds, DogBreedsAdmin)





class PaymentAdmin(admin.ModelAdmin):
    model = Payment
    list_display = ['payment_type', 'advertisement', 'amount', 'date_time_paid', 'payer_alias']
    list_display_links = ['payment_type']

admin.site.register(Payment, PaymentAdmin)

class PaymentInline(admin.TabularInline):
    model = Payment
    extra = 0

class AdvertisementAdmin(admin.ModelAdmin):
    form = NewAdTakeMyDogFormAdmin
    list_display = ['title', 'is_offering_own_dog', 'author', 'name', 'is_published']
    list_display_links = ['title']
    readonly_fields = ('id',)
    inlines = [
        PaymentInline,
    ]

admin.site.register(Advertisement, AdvertisementAdmin)





class SiteAdmin(admin.ModelAdmin):
    list_display = ('id', 'domain', 'name')
    search_fields = ('id', 'domain', 'name')


admin.site.unregister(Site)
admin.site.register(Site, SiteAdmin)