from django.core.management.base import BaseCommand
from django.db import connections
from django.db.utils import OperationalError
import time


class Command(BaseCommand):
    """Waits for the database to be available before continuing"""

    def handle(self, *args, **options) -> None:
        self.stdout.write(self.style.WARNING("Waiting for the database..."))
        db_connection = None
        while not db_connection:
            try:
                db_connection = connections["default"]
            except OperationalError:
                self.stdout.write(
                    "Database not available, waiting for 1 second..."
                )
                time.sleep(1)
        self.stdout.write(self.style.SUCCESS("Database available!"))
