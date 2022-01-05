from io import open_code
from django.db import models
from django.contrib.auth import get_user_model

from common.abstracts import SoftDeleteModel, TimeStampedModel

User = get_user_model()

# Create your models here.

class Province(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

class Municipality(models.Model):
    province = models.ForeignKey(Province, on_delete=models.CASCADE)
    name= models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Area(models.Model):
    province = models.ForeignKey(Province, on_delete=models.CASCADE, null=True)
    municipality = models.ForeignKey(Municipality, on_delete=models.CASCADE)
    name= models.CharField(max_length=100)

    def __str__(self):
        return self.name

class DogSizeChoices(models.Model):
    size = models.CharField(max_length=20) 

    def __str__(self):
        return self.size


class DogBreeds(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name


class Advertisement(SoftDeleteModel, TimeStampedModel):

    # Foreign keys
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    province = models.ForeignKey(Province, on_delete=models.CASCADE, verbose_name='Landskap')
    municipality = models.ForeignKey(Municipality, on_delete=models.CASCADE, verbose_name='Kommun')
    area = models.ForeignKey(Area, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Område')

    # Choices declaration
    DAYS_PER_WEEK_CHOICES = (
        ("1", "1 dag per vecka"),
        ("1-5", "1-2 dagar per vecka"),
        ("1-3", "1-3 dagar per vecka"),
        ("1-4", "1-4 dagar per vecka"),
        ("1-5", "1-5 dagar per vecka"),
    )

    # Choices declaration
    PAYMENT_CHOICES = (
        ("S", "Swish"),
        ("B", "Bankgiro"),
    )


    # Dog details
    name = models.CharField(max_length=50, verbose_name='Hundens namn', default='')
    age = models.IntegerField(verbose_name='Hundens ålder (år)', default=0)

    # Payment status
    is_published = models.BooleanField(default=False, null=True)
    payment_type = models.CharField(max_length=1, choices=PAYMENT_CHOICES, default=1, verbose_name='Betalningsmetod', null=True)


    # Type of Ad (Offering own dog or requesting a dog)
    is_offering_own_dog = models.BooleanField(null=True)

    # String data
    title = models.CharField(max_length=150, verbose_name='Annons-Titel')
    description = models.TextField(max_length=1500, verbose_name='Annons-beskrivning')
    
    # Choices
    days_per_week = models.CharField(max_length=3, choices=DAYS_PER_WEEK_CHOICES, default=1, verbose_name='Önskad omfattning')
    hundras = models.ForeignKey(DogBreeds, on_delete=models.CASCADE, null=True, verbose_name=u'Hundras')
    size_offered = models.ForeignKey(DogSizeChoices, verbose_name='Hundens storlek', on_delete=models.CASCADE, related_name='size_offered', null=True)
    size_requested = models.ManyToManyField(DogSizeChoices, verbose_name='Önskade hundstorlekar (flerval)', related_name='size_requested')

    # Images
    image1 = models.ImageField(null=True, blank=True, verbose_name="Bild 1")
    image2 = models.ImageField(null=True, blank=True, verbose_name="Bild 2")
    image3 = models.ImageField(null=True, blank=True, verbose_name="Bild 3")


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

    @property
    def has_initial_payment(self):
        if Payment.objects.filter(advertisement=self, payment_type=1).exists():
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


