from django.core.management.base import BaseCommand
from django.db import connections
from django.db.utils import OperationalError
import time


class Command(BaseCommand):
    help = "Waits for the database to be available before continuing"

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING("Waiting for the database..."))

        max_retries = 10
        delay = 1

        for attempt in range(1, max_retries + 1):
            try:
                connection = connections["default"]
                connection.ensure_connection()
                cursor = connection.cursor()
                cursor.execute("SELECT 1")
                cursor.close()

                self.stdout.write(self.style.SUCCESS("Database is ready!"))
                return
            except OperationalError:
                self.stdout.write(
                    f"Attempt {attempt}/{max_retries}: Database unavailable, retrying in {delay} sec..."
                )
                time.sleep(delay)
        self.stdout.write(
            self.style.ERROR("Max retries reached. Database is still unavailable.")
        )
