from io import open_code
import datetime
from datetime import timedelta, datetime
import uuid
from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.fields import BooleanField, CharField, IntegerField
from django.db.models.fields.related import ForeignKey, ManyToManyField
from django.forms.fields import UUIDField

from stdimage import StdImageField

from common.abstracts import SoftDeleteModel, TimeStampedModel


# Supportive functions

User = get_user_model()

def get_30_days_ahead():
    return datetime.today() + timedelta(days=30)

def get_30_days_ahead_from_date_obj(date_obj):
    return date_obj + timedelta(days=30)



# Create your models here.

class Province(models.Model):
    name = models.CharField(max_length=30)
    offering_count = models.IntegerField(default=0)
    requesting_count = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.name} ({self.offering_count}, {self.requesting_count})'

class Municipality(models.Model):
    province = models.ForeignKey(Province, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    offering_count = models.IntegerField(default=0)
    requesting_count = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.name} ({self.offering_count}, {self.requesting_count})'

class Area(models.Model):
    province = models.ForeignKey(Province, on_delete=models.CASCADE, null=True)
    municipality = models.ForeignKey(Municipality, on_delete=models.CASCADE)
    name= models.CharField(max_length=100)
    offering_count = models.IntegerField(default=0)
    requesting_count = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.name} ({self.offering_count}, {self.requesting_count})'


class NewsEmail(models.Model):

    INTERVAL_CHOICES = (
        (1, "Veckovis"),
        (2, "Dagligen"),
    )

    AD_TYPES_CHOICES = (
        (1, "Erbjudes"),
        (2, "Sökes"),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    province = ForeignKey(Province, on_delete=models.CASCADE, verbose_name='Landskap/Storstad', null=True, blank=True)
    municipality = ForeignKey(Municipality, on_delete=models.CASCADE, verbose_name='Kommun', null=True, blank=True)
    areas = ManyToManyField(Area, verbose_name='Område', blank=True)
    interval = IntegerField(choices=INTERVAL_CHOICES, null=True, blank=True, verbose_name='Intervall')
    ad_type = IntegerField(choices=AD_TYPES_CHOICES, null=True, blank=True, verbose_name='Annonstyp')
    is_active = BooleanField(default=False)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    def __str__(self):
        return f'{self.user} {self.interval}'

    @staticmethod
    def get_all_active_subscriptions():
        return NewsEmail.objects.filter(is_active=True)

    @staticmethod
    def get_all_active_daily_subscriptions(ad_type: str):
        if ad_type == 'offering':
            return NewsEmail.objects.filter(is_active=True, ad_type=1, interval=2)
        if ad_type == 'requesting':
            return NewsEmail.objects.filter(is_active=True, ad_type=2, interval=2)

    @staticmethod
    def get_all_active_weekly_subscriptions(ad_type: str):
        if ad_type == 'offering':
            return NewsEmail.objects.filter(is_active=True, ad_type=1, interval=1)
        if ad_type == 'requesting':
            return NewsEmail.objects.filter(is_active=True, ad_type=2, interval=1)


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

class Advertisement(SoftDeleteModel, TimeStampedModel):

    # Foreign keys
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    province = models.ForeignKey(Province, on_delete=models.CASCADE, verbose_name='Landskap/Storstad')
    municipality = models.ForeignKey(Municipality, on_delete=models.CASCADE, verbose_name='Kommun')
    area = models.ForeignKey(Area, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Område')

    # Choices declaration


    # Choices declaration
    PAYMENT_CHOICES = (
        ("S", "Swish"),
        ("B", "Bankgiro"),
    )


    # Ad life-time
    deletion_date = models.DateField(default=get_30_days_ahead)

    # Dog details
    name = models.CharField(max_length=50, verbose_name='Hundens namn', default='')
    age = models.IntegerField(verbose_name='Hundens ålder (år)', default=0)

    # Status
    is_published = models.BooleanField(default=False, null=True)
    is_deleted = models.BooleanField(default=False, null=True)

    # Payment status
    payment_type = models.CharField(max_length=1, choices=PAYMENT_CHOICES, default=1, verbose_name='Betalningsmetod', null=True)

    # Type of Ad (Offering own dog or requesting a dog)
    is_offering_own_dog = models.BooleanField(null=True)

    # String data
    title = models.CharField(max_length=150, verbose_name='Annons-Titel')
    description = models.TextField(max_length=1500, verbose_name='Annons-beskrivning')
    
    # Choices
    days_per_week = models.CharField(max_length=3, choices=DAYS_PER_WEEK_CHOICES, default=1, verbose_name='Önskad omfattning')
    hundras = models.ForeignKey(DogBreed, on_delete=models.CASCADE, null=True, verbose_name=u'Hundras')
    size_offered = models.ForeignKey(DogSizeChoice, verbose_name='Hundens storlek', on_delete=models.CASCADE, related_name='size_offered', null=True)
    size_requested = models.ManyToManyField(DogSizeChoice, verbose_name='Önskade hundstorlekar (flerval)', related_name='size_requested')

    # Images
    image1 = StdImageField(null=True, blank=True, verbose_name="Bild 1", upload_to=content_file_name, variations={'thumbnail': {'width': 600, 'height': 800}})
    image2 = StdImageField(null=True, blank=True, verbose_name="Bild 2", upload_to=content_file_name, variations={'thumbnail': {'width': 600, 'height': 800}})
    image3 = StdImageField(null=True, blank=True, verbose_name="Bild 3", upload_to=content_file_name, variations={'thumbnail': {'width': 600, 'height': 800}})
   
    ad_views = models.IntegerField(default=0)

    def __str__(self):
        return self.title


    def create_payment(self, payment_type, amount, payment_reference, date_time_paid, payer_alias):
        
        new_payment = Payment.objects.create(
            advertisement=self,
            payment_type=payment_type,
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
        return Advertisement.objects.filter(is_published=True, is_deleted=False, is_offering_own_dog=True)

    @staticmethod
    def get_all_active_requesting_ads():
        return Advertisement.objects.filter(is_published=True, is_deleted=False, is_offering_own_dog=False)

    @property
    def has_initial_payment(self):
        if Payment.objects.filter(advertisement=self, payment_type=1).exists():
            return True
        else:
            return False

    @property
    def has_extended_payment(self):
        if Payment.objects.filter(advertisement=self, payment_type=2).exists():
            return True
        else:
            return False


class Payment(models.Model):

    PAYMENT_TYPES = (
        ("1", "Initial payment"),
        ("2", "Extend ad run-time payment"),
        ("3", "Other"),
    )

    advertisement = models.ForeignKey(Advertisement, on_delete=models.CASCADE, verbose_name='advertisement')
    payment_type = models.CharField(max_length=1, choices=PAYMENT_TYPES, default=1, verbose_name='payment_type')
    amount = models.IntegerField()
    payment_reference = models.CharField(max_length=50)
    date_time_paid = models.DateTimeField()
    payer_alias = models.CharField(max_length=50, null=True)


    def __str__(self):
        return self.payer_alias
        


