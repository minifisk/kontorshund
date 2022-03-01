from io import open_code
import datetime
import uuid
from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.fields import BooleanField, CharField, IntegerField
from django.db.models.fields.related import ForeignKey, ManyToManyField
from django.forms.fields import UUIDField
from dateutil.relativedelta import *


from stdimage import StdImageField

from common.abstracts import SoftDeleteModel, TimeStampedModel


# Supportive functions

User = get_user_model()

def get_one_month_ahead_from_today():
    new_date = datetime.date.today() + relativedelta(months=+1)
    return new_date

def get_one_month_ahead_from_date_obj(date_obj):
    return date_obj + relativedelta(months=+1)



# Create your models here.

class Province(models.Model):
    name = models.CharField(max_length=30)
    offering_count = models.IntegerField(default=0)
    requesting_count = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class Municipality(models.Model):
    province = models.ForeignKey(Province, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    offering_count = models.IntegerField(default=0)
    requesting_count = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class Area(models.Model):
    province = models.ForeignKey(Province, on_delete=models.CASCADE)
    municipality = models.ForeignKey(Municipality, on_delete=models.CASCADE)
    name= models.CharField(max_length=100)
    offering_count = models.IntegerField(default=0)
    requesting_count = models.IntegerField(default=0)

    def __str__(self):
        return self.name

from django.utils.translation import gettext_lazy as _


class IntervalChoices(models.TextChoices):
    WEEKLY = "WK", _('Veckovis')
    DAILY = "DL", _('Dagligen')

class AdTypesChoices(models.TextChoices):
    OFFERING = "OF", _('Erbjudes')
    REQUESTING = "RQ",  _('Sökes')

class NewsEmail(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    province = ForeignKey(Province, on_delete=models.CASCADE, verbose_name='Landskap/Storstad', null=True, blank=True)
    municipality = ForeignKey(Municipality, on_delete=models.CASCADE, verbose_name='Kommun', null=True, blank=True)
    areas = ManyToManyField(Area, verbose_name='Område', blank=True)

    interval = CharField(max_length=2, choices=IntervalChoices.choices, default=IntervalChoices.WEEKLY, verbose_name='Intervall')
    ad_type = CharField(max_length=2, choices=AdTypesChoices.choices, default=AdTypesChoices.OFFERING, verbose_name='Annonstyp')

    is_active = BooleanField(default=False)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    def __str__(self):
        return f'{self.user} {self.interval}'

    @staticmethod
    def get_all_active_subscriptions():
        return NewsEmail.objects.filter(is_active=True)

    @staticmethod
    def get_all_active_daily_subscriptions(ad_type):
        return NewsEmail.objects.filter(is_active=True, ad_type=ad_type, interval=IntervalChoices.DAILY)

    @staticmethod
    def get_all_active_weekly_subscriptions(ad_type):
        return  NewsEmail.objects.filter(is_active=True, ad_type=ad_type, interval=IntervalChoices.WEEKLY)



class DogSizeChoice(models.Model):
    size = models.CharField(max_length=20) 

    def __str__(self):
        return self.size


class DogBreed(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name


def content_file_name(instance, filename):
    return '/'.join(['content', instance.author.username, filename])


DAYS_PER_WEEK_CHOICES = (
    ("1", "1 dag per vecka"),
    ("1-2", "1-2 dagar per vecka"),
    ("1-3", "1-3 dagar per vecka"),
    ("1-4", "1-4 dagar per vecka"),
    ("1-5", "1-5 dagar per vecka"),
)

class AdKind(models.TextChoices):
    OFFERING = 'OF', 'Offering',
    REQUESTING = 'RQ', 'Requesting',


class Advertisement(SoftDeleteModel, TimeStampedModel):

    PAYMENT_CHOICES = (
        ("S", "Swish"),
        ("B", "Bankgiro"),
    )

    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Författare')
    province = models.ForeignKey(Province, on_delete=models.CASCADE, verbose_name='Landskap/Storstad')
    municipality = models.ForeignKey(Municipality, on_delete=models.CASCADE, verbose_name='Kommun')
    area = models.ForeignKey(Area, on_delete=models.CASCADE, verbose_name='Område', null=True, blank=True,)

    ad_kind = models.CharField(max_length=2, choices=AdKind.choices, default=AdKind.OFFERING, verbose_name='Annonstyp')
    
    is_published = models.BooleanField(default=False, verbose_name='Publicerad')
    is_deleted = models.BooleanField(default=False, verbose_name='Borttagen')

    deletion_date = models.DateField(default=get_one_month_ahead_from_today, verbose_name='Borttagnings-datum')
    ad_views = models.IntegerField(default=0, verbose_name='Visningar')
    name = models.CharField(max_length=50, verbose_name='Hundens namn', default='')
    age = models.IntegerField(verbose_name='Hundens ålder (år)', default=0)
    title = models.CharField(max_length=150, verbose_name='Annons-Titel')
    description = models.TextField(max_length=1500, verbose_name='Annons-beskrivning')
    days_per_week = models.CharField(max_length=3, choices=DAYS_PER_WEEK_CHOICES, default=1, verbose_name='Önskad omfattning')
    hundras = models.ForeignKey(DogBreed, on_delete=models.CASCADE, verbose_name=u'Hundras', null=True,)
    size_offered = models.ForeignKey(DogSizeChoice, verbose_name='Hundens storlek', on_delete=models.CASCADE, related_name='size_offered', null=True)
    size_requested = models.ManyToManyField(DogSizeChoice, verbose_name='Önskade hundstorlekar (flerval)', related_name='size_requested')

    payment_choice = models.CharField(max_length=1, choices=PAYMENT_CHOICES, default=1, verbose_name='Betalningsmetod')
    
    image1 = StdImageField(verbose_name="Bild 1", upload_to=content_file_name, variations={'thumbnail': {'width': 600, 'height': 800}}, null=True, blank=True)
    image2 = StdImageField(verbose_name="Bild 2", upload_to=content_file_name, variations={'thumbnail': {'width': 600, 'height': 800}}, null=True, blank=True)
    image3 = StdImageField(verbose_name="Bild 3", upload_to=content_file_name, variations={'thumbnail': {'width': 600, 'height': 800}}, null=True, blank=True)
   

    def __str__(self):
        return self.title


    def create_payment(
        self,
        payment_kind,
        amount,
        payment_reference,
        date_time_paid,
        payer_alias
    ):
        
        new_payment = Payment.objects.create(
            advertisement=self,
            payment_kind=payment_kind,
            amount=amount,
            payment_reference=payment_reference,
            date_time_paid=date_time_paid,
            payer_alias=payer_alias
        )

        return new_payment

    @staticmethod
    def get_all_active_ads():
        return Advertisement.objects.filter(is_published=True, is_deleted=False)

    @staticmethod
    def get_all_active_offering_ads():
        return Advertisement.objects.filter(is_published=True, is_deleted=False, ad_kind='OF')

    @staticmethod
    def get_all_active_requesting_ads():
        return Advertisement.objects.filter(is_published=True, is_deleted=False, ad_kind='RQ')

    @property
    def has_initial_payment(self):
        if Payment.objects.filter(advertisement=self, payment_kind=PaymentKind.INITIAL).exists():
            return True
        else:
            return False

    @property
    def has_extended_payment(self):
        if Payment.objects.filter(advertisement=self, payment_kind=PaymentKind.EXTENDED).exists():
            return True
        else:
            return False

class PaymentKind(models.TextChoices):
    INITIAL = 'IN', 'Initial',
    EXTENDED = 'EX', 'Extended',


class Payment(models.Model):


    advertisement = models.ForeignKey(Advertisement, on_delete=models.CASCADE, verbose_name='advertisement')
    payment_kind = models.CharField(max_length=2, choices=PaymentKind.choices, default=PaymentKind.INITIAL, verbose_name='Betalningstyp')
    amount = models.IntegerField()
    payment_reference = models.CharField(max_length=50)
    date_time_paid = models.DateTimeField()
    payer_alias = models.CharField(max_length=50)


    def __str__(self):
        return self.payer_alias
        


