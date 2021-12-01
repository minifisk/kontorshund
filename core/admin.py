from django.contrib import admin

from core.models import Province, Municipality, Advertisement, Area

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



class AdvertisementAdmin(admin.ModelAdmin):
    model = Advertisement

admin.site.register(Advertisement, AdvertisementAdmin)