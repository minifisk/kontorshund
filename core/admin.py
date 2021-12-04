from django.contrib import admin

from core.models import Province, Municipality, Advertisement, Area, DogSizeChoices, DogBreeds
from core.forms import NewAdTakeMyDogForm

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


class AdvertisementAdmin(admin.ModelAdmin):
    form = NewAdTakeMyDogForm

admin.site.register(Advertisement, AdvertisementAdmin)