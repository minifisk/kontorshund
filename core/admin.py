from django.contrib import admin
from django.contrib.sites.models import Site

from core.models import Payment, Province, Municipality, Advertisement, Area, DogSizeChoice, DogBreed
from core.forms import NewAdTakeMyDogForm, NewAdFormAdmin, NewsEmailFormAdmin
from core.models import NewsEmail

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
    model = DogSizeChoice

admin.site.register(DogSizeChoice, DogSizeAdmin)


class DogBreedAdmin(admin.ModelAdmin):
    model = DogBreed

admin.site.register(DogBreed, DogBreedAdmin)



class PaymentAdmin(admin.ModelAdmin):
    model = Payment
    list_display = ['id', 'payment_type', 'advertisement', 'amount', 'date_time_paid', 'payer_alias']
    list_display_links = ['id']

admin.site.register(Payment, PaymentAdmin)

class PaymentInline(admin.TabularInline):
    model = Payment
    extra = 0

class AdvertisementAdmin(admin.ModelAdmin):
    form = NewAdFormAdmin
    list_display = ['is_published', 'is_deleted',  'is_offering_own_dog', 'deletion_date', 'id', 'title', 'author', 'name']
    list_display_links = ['title']
    readonly_fields = ('id',)
    inlines = [
        PaymentInline,
    ]

admin.site.register(Advertisement, AdvertisementAdmin)


class NewsEmailAdmin(admin.ModelAdmin):
    form = NewsEmailFormAdmin
    list_display = ['user', 'province', 'municipality', 'interval', 'ad_type']
    readonly_fields = ('id',)

admin.site.register(NewsEmail, NewsEmailAdmin)



class SiteAdmin(admin.ModelAdmin):
    list_display = ('id', 'domain', 'name')
    search_fields = ('id', 'domain', 'name')


admin.site.unregister(Site)
admin.site.register(Site, SiteAdmin)