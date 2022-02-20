from django.contrib import admin
from django.contrib.sites.models import Site

from core.models import Payment, Province, Municipality, Advertisement, Area, DogSizeChoice, DogBreed
from core.forms.ad_forms import AdFormAdmin
from core.forms.news_email_form import NewsEmailFormAdmin
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
    form = AdFormAdmin
    list_display = ['pk', 'is_published', 'is_deleted',  'title', 'ad_kind', 'deletion_date', 'created_at',  'author']
    list_display_links = ['title']
    readonly_fields = ('id', 'created_at', 'updated_at', 'ad_views')
    save_as = True
    list_filter = ('is_deleted', 'is_published',)
    fieldsets = (
        ('Ad details', {'fields': ('is_published', 'is_deleted', 'deletion_date')}),
        ('Geographical', {'fields': ('province', 'municipality', 'area')}),
        ('General', {'fields': ('author', 'ad_kind', 'title', 'description', 'days_per_week', 'image1', 'image2', 'image3')}),
        ('Offering-fields', {'fields': ('size_offered', 'name', 'age', 'hundras')}),
        ('Requesting-fields', {'fields': ('size_requested',)}),
        ('Chosen payment type', {'fields': ('payment_type',)}),
    )
    inlines = [
        PaymentInline,
    ]
    search_fields = ('title', 'description',)
    ordering = ('pk',)

admin.site.register(Advertisement, AdvertisementAdmin)

class NewsEmailAdmin(admin.ModelAdmin):
    form = NewsEmailFormAdmin
    list_display = ['is_active', 'user', 'province', 'municipality', 'interval', 'ad_type']
    list_display_links = ['user']
    readonly_fields = ('id', 'uuid')

admin.site.register(NewsEmail, NewsEmailAdmin)

class SiteAdmin(admin.ModelAdmin):
    list_display = ('id', 'domain', 'name')
    search_fields = ('id', 'domain', 'name')

admin.site.unregister(Site)
admin.site.register(Site, SiteAdmin)