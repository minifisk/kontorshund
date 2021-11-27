from django.contrib import admin

from core.models import Province, Municipality, Advertisement
from core.forms import AdvertisementForm

# Register your models here.

class ProvinceAdmin(admin.ModelAdmin):
    model = Province

admin.site.register(Province, ProvinceAdmin)


class MunicipalityAdmin(admin.ModelAdmin):
    model = Municipality

admin.site.register(Municipality, MunicipalityAdmin)


class AdvertisementAdmin(admin.ModelAdmin):
    model = Advertisement

admin.site.register(Advertisement, AdvertisementAdmin)