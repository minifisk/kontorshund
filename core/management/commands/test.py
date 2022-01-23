from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    help = 'Testing'

    def handle(self, *args, **options):
        from django.contrib.auth import get_user_model
        User = get_user_model()
        print(User.objects.all().count())