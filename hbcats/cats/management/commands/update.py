from django.core.management.base import BaseCommand  # , CommandError
from cats.updatecats import UpdateCats
# from cats.models import Cats


class Command(BaseCommand):
    help = "Updates the database with latest cat adopted and arrivals"

    def handle(self, *args, **options):
        UpdateCats().update_cats()
        self.stdout.write(self.style.SUCCESS("Successfully updated cats"))
