from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _

from accounts.managers import UserManager

from core import models as core_models

# Create your models here.


# https://testdriven.io/blog/django-custom-user-model/
class CustomUser(AbstractBaseUser, PermissionsMixin):
    """ 
        Custom User-model, where email-field is set as default authentication field.
    """
    
    email = models.EmailField(_('email address'), unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        news_email_obj = core_models.NewsEmail.objects.filter(user=self)
        if not news_email_obj.exists():
            new_news_email_obj = core_models.NewsEmail.objects.create(user=self)

    def __str__(self):
        return self.email