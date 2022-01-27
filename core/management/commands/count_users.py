from django.core.management.base import BaseCommand, CommandError
from core.models import Advertisement


class Command(BaseCommand):
    help = 'Updating offering & requesting count on Province, Municipality and Area'

    def handle(self, *args, **options):
        all_adv = Advertisement.objects.all().count()
        print('Number of advertisements: ', all_adv)