
from core.models import Advertisement, DogBreed, DogSizeChoice, Municipality, Province
from random import randint

# Create X unpublished ads to Y user

def create_offering_ads(count=1, user=None, is_published=False):
    r_high = randint(1,300)
    r_low = randint(1,20)

    province = Province.objects.get(name='Stockholm')
    municipality = Municipality.objects.get(name='Stockholms stad')
    breed = DogBreed.objects.get(pk=5)
    size_offered = DogSizeChoice.objects.get(pk=1)
    
    ads = []

    for i in range(count):
        ads.append(
            Advertisement.objects.create(
            is_offering_own_dog=True,
            author=user,
            province=province,
            municipality=municipality,
            name=f'Frasse {r_high}',
            age=r_low,
            is_published=is_published,
            is_deleted=False,
            title=f'Hund erbjudes {r_high}',
            description=f'Hejsan här kommer en ny annons {r_high}',
            hundras=breed,  
            days_per_week=1,
            size_offered=size_offered,
            )
        )   

    return ads


def create_requesting_ads(count=1, user=None, is_published=False):
    r_high = randint(1,300)

    province = Province.objects.get(name='Stockholm')
    municipality = Municipality.objects.get(name='Stockholms stad')
    size_requested = DogSizeChoice.objects.get(pk=1)
    
    ads = []

    for i in range(count):
        ads.append(
            Advertisement.objects.create(
            is_offering_own_dog=False,
            author=user,
            province=province,
            municipality=municipality,
            is_published=is_published,
            is_deleted=False,
            title=f'Hund sökes {r_high}',
            description=f'Hejsan här kommer en ny annons {r_high}',
            days_per_week=1,
            size_offered=size_requested,
            )
        )   

    return ads

