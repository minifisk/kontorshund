import pytz
from datetime import datetime
from core.models import Advertisement, Area, DogBreed, DogSizeChoice, Municipality, Province
from random import randint
from django.core.files import File
import os

from django.core.files.uploadedfile import SimpleUploadedFile

from core.models import Payment, PaymentKind, AdKind
from core.models import get_one_month_ahead_from_today
from core.models import NewsEmail




# Create X unpublished ads to Y user

def create_offering_ads(
    count=1,
    user=None,
    province=None,
    municipality=None,
    area=None,
    is_published=False,
    created_at=None,
    deletion_date='2023-01-01',
    ):

    r_high = randint(1,300)
    r_low = randint(1,20)

    breed = DogBreed.objects.get(pk=5)
    size_offered = DogSizeChoice.objects.get(pk=1)
    
    ads = []

    for i in range(count):
        ad = Advertisement.objects.create(
            ad_kind=AdKind.OFFERING,
            author=user,
            province=province,
            municipality=municipality,
            area=area,
            name=f'Frasse {r_high}',
            age=r_low,
            is_published=is_published,
            is_deleted=False,
            deletion_date=deletion_date,
            title=f'Hund erbjudes {r_high}',
            description=f'Hejsan här kommer en ny annons {r_high}',
            hundras=breed,  
            days_per_week=1,
            size_offered=size_offered,
        )

        ad.save()
        if created_at:
            ad.created_at = created_at
            ad.save()
        ads.append(ad)  

    return ads


def create_requesting_ads(
    count=1,
    user=None,
    province=None,
    municipality=None,
    area=None,
    is_published=False,
    created_at=None,
    deletion_date='2023-01-01',
    ):

    r_high = randint(1,300)

    size_requested = DogSizeChoice.objects.get(pk=1)
    
    ads = []

    for i in range(count):
        ad = Advertisement.objects.create(
            ad_kind=AdKind.REQUESTING,
            created_at=created_at,
            author=user,
            province=province,
            municipality=municipality,
            area=area,
            is_published=is_published,
            is_deleted=False,
            title=f'Hund sökes {r_high}',
            description=f'Hejsan här kommer en ny annons {r_high}',
            days_per_week=1,
        )

        ad.save()
        if created_at:
            ad.created_at = created_at
            ad.save()
        ad.size_requested.add(size_requested)

        ads.append(ad)  

    return ads





def create_offering_adss_stockholm_stockholms_stad(count=1, user=None, is_published=False, created_at=None):
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
                ad_kind=AdKind.OFFERING,
                created_at=created_at,
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


def create_offering_adss_stockholm_stockholm_stad_katarina_sofia(count=1, user=None, is_published=False):
    r_high = randint(1,300)
    r_low = randint(1,20)

    province = Province.objects.get(name='Stockholm')
    municipality = Municipality.objects.get(name='Stockholms stad')
    area = Area.objects.get(name='Katarina, Sofia')
    breed = DogBreed.objects.get(pk=5)
    size_offered = DogSizeChoice.objects.get(pk=1)
    
    ads = []

    for i in range(count):
        ads.append(
            Advertisement.objects.create(
                ad_kind=AdKind.OFFERING,
                author=user,
                province=province,
                municipality=municipality,
                area=area,
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


def create_requesting_ads_stockholm_stockholms_stad(count=1, user=None, is_published=False):
    r_high = randint(1,300)

    province = Province.objects.get(name='Stockholm')
    municipality = Municipality.objects.get(name='Stockholms stad')
    size_requested = DogSizeChoice.objects.get(pk=1)
    
    ads = []

    for i in range(count):
        ads.append(
            Advertisement.objects.create(
                ad_kind=AdKind.REQUESTING,
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


def create_offering_adss_halland_falkenberg(count=1, user=None, is_published=False):
    r_high = randint(1,300)
    r_low = randint(1,20)

    province = Province.objects.get(name='Halland')
    municipality = Municipality.objects.get(name='Falkenberg')
    breed = DogBreed.objects.get(pk=5)
    size_offered = DogSizeChoice.objects.get(pk=1)
    
    ads = []

    for i in range(count):
        ads.append(
            Advertisement.objects.create(
                ad_kind=AdKind.OFFERING,
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


def create_offering_adss_halland_halmstad(count=1, user=None, is_published=False):
    r_high = randint(1,300)
    r_low = randint(1,20)

    province = Province.objects.get(name='Halland')
    municipality = Municipality.objects.get(name='Halmstad')
    breed = DogBreed.objects.get(pk=5)
    size_offered = DogSizeChoice.objects.get(pk=1)
    
    ads = []

    for i in range(count):
        ads.append(
            Advertisement.objects.create(
                ad_kind=AdKind.OFFERING,
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


def create_ad_without_payment(count=1, user=None, is_published=False):
    r_high = randint(1,300)
    r_low = randint(1,20)

    province = Province.objects.get(name='Stockholm')
    municipality = Municipality.objects.get(name='Stockholms stad')
    breed = DogBreed.objects.get(pk=5)
    size_offered = DogSizeChoice.objects.get(pk=1)
    
    ad = Advertisement.objects.create(
        ad_kind=AdKind.OFFERING,
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

    return ad

def create_ad_with_initial_payment(count=1, user=None, is_published=True, deletion_date=get_one_month_ahead_from_today()):
    r_high = randint(1,300)
    r_low = randint(1,20)

    province = Province.objects.get(name='Stockholm')
    municipality = Municipality.objects.get(name='Stockholms stad')
    breed = DogBreed.objects.get(pk=5)
    size_offered = DogSizeChoice.objects.get(pk=1)
    
    ad = Advertisement.objects.create(
        ad_kind=AdKind.OFFERING,
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
        deletion_date=deletion_date,
        )

    Payment.objects.create(
        advertisement=ad,
        payment_kind=PaymentKind.INITIAL,
        amount=30,
        payment_reference=r_high,
        date_time_paid=datetime.now(pytz.utc),
        payer_alias=r_high
    )

    return ad




def create_ad_with_extended_payment(count=1, user=None, is_published=True, deletion_date=get_one_month_ahead_from_today()):
    r_high = randint(1,300)
    r_low = randint(1,20)

    province = Province.objects.get(name='Stockholm')
    municipality = Municipality.objects.get(name='Stockholms stad')
    breed = DogBreed.objects.get(pk=5)
    size_offered = DogSizeChoice.objects.get(pk=1)
    
    ad = Advertisement.objects.create(
        ad_kind=AdKind.OFFERING,
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
        deletion_date=deletion_date
        )

    Payment.objects.create(
        advertisement=ad,
        payment_kind=PaymentKind.EXTENDED,
        amount=30,
        payment_reference=r_high,
        date_time_paid=datetime.now(pytz.utc),
        payer_alias=r_high
    )

    return ad


def create_swish_callback_payload(self, id='123456', ad_id=None, error_message='', status='PAID', error_code=''):
    return {
        'id': id,
        'payeePaymentReference': ad_id,
        'paymentReference': 'A05B3CFC615143798F9DF8509E39C9B8',
        'callbackUrl': 'https://kontorshund.se/swish/callback',
        'payerAlias': '46721506520',
        'payeeAlias': '1233473337',
        'currency': 'SEK',
        'message': 'Betalning för annons med ID 3',
        'errorMessage': error_message,
        'status': status,
        'amount': 1.0,
        'dateCreated': '2022-02-22T19:26:03.619Z',
        'datePaid': '2022-02-22T19:26:14.826Z',
        'errorCode': error_code
}

def create_news_email(province, municipality, user, ad_type, is_active, interval, areas=None,):


    news_email_obj = NewsEmail.objects.create(
        user=user,
        province=province[0],
        municipality=municipality[0],
        interval=interval,
        ad_type=ad_type,
        is_active=is_active,
    )

    for area in areas:
        news_email_obj.add(area)

    return news_email_obj