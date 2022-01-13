import uuid 

from django.db import models
from django.contrib.auth.models import AbstractUser

from core import models as core_models

# Create your models here.

class CustomUser(AbstractUser):
    pass

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        news_email_obj = core_models.NewsEmail.objects.filter(user=self)
        if not news_email_obj.exists():
            new_news_email_obj = core_models.NewsEmail.objects.create(user=self)

    def __str__(self):
        return self.email
