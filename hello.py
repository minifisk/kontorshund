

from django.db import connection
from django.conf import settings

settings.configure()

from core.models import Advertisement

count = Advertisement.objects.all().count()

print('Number of advertisements: ', count)