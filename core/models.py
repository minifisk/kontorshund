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

    # Choices declaration
    DAYS_PER_WEEK_CHOICES = (
        ("1", "1 dag per vecka"),
        ("1-5", "1-2 dagar per vecka"),
        ("1-3", "1-3 dagar per vecka"),
        ("1-4", "1-4 dagar per vecka"),
        ("1-5", "1-5 dagar per vecka"),
    )

    # Foreign keys
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    province = models.ForeignKey(Province, on_delete=models.CASCADE, verbose_name='Landskap')
    municipality = models.ForeignKey(Municipality, on_delete=models.CASCADE, verbose_name='Kommun')
    area = models.ForeignKey(Area, on_delete=models.CASCADE, null=True, verbose_name='Område')

    # Type of Ad (Offering own dog or requesting a dog)
    is_offering_own_dog = models.BooleanField()

    # String data
    title = models.CharField(max_length=150, verbose_name='Titel')
    description = models.CharField(max_length=500, verbose_name='Beskrivning')
    
    # Choices
    days_per_week = models.CharField(max_length=3, choices=DAYS_PER_WEEK_CHOICES, default=1, verbose_name='Omfattning')
    breed = models.ForeignKey(DogBreeds, on_delete=models.CASCADE, null=True, verbose_name='Hundras')
    size_offered = models.ForeignKey(DogSizeChoices, verbose_name='Min hunds storlek', on_delete=models.CASCADE, related_name='size_offered', null=True)
    size_requested = models.ManyToManyField(DogSizeChoices, verbose_name='Möjliga hundstorlekar', related_name='size_requested')


    # Images
    image1 = models.ImageField(null=True, blank=True)
    image2 = models.ImageField(null=True, blank=True)
    image3 = models.ImageField(null=True, blank=True)


    def __str__(self):
        return self.title



