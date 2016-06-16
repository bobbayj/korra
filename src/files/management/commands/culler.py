from django.core.management.base import BaseCommand
from django.utils import timezone

from ...models import File


class Command(BaseCommand):

    help = "Deletes files that have past expiry."

    def handle(self, *args, **options):
        for f in File.objects.filter(expires__lte=timezone.now()):
            f.delete()
