import os
import csv
from django.core.management.base import BaseCommand
from lookups.models import City, State


class Command(BaseCommand):
    help = "Populate City model from CSV file"

    def handle(self, *args, **kwargs):
        file_path = os.path.join("lookups", "fixtures", "city.csv")

        with open(file_path, "r", encoding="utf-8") as file:
            reader = csv.reader(file)

            # Skip the header row if there is one
            next(reader, None)

            for row in reader:
                if len(row) < 6:
                    self.stdout.write(
                        self.style.ERROR(f"Invalid row data: {row}. Skipping.")
                    )
                    continue

                try:
                    (
                        id,
                        name,
                        state_id,
                        latitude,
                        longitude,
                        country_code,
                        country_id,
                    ) = row

                    state = State.objects.get(id=state_id)

                    city, created = City.objects.get_or_create(
                        name=name,
                        state=state,
                        country_id=country_id,
                        country_code=country_code,
                        latitude=float(latitude),
                        longitude=float(longitude),
                    )

                    if created:
                        self.stdout.write(
                            self.style.SUCCESS(f"City '{name}' added successfully.")
                        )
                    else:
                        self.stdout.write(
                            self.style.SUCCESS(f"City '{name}' already exists.")
                        )

                except State.DoesNotExist:
                    self.stdout.write(
                        self.style.ERROR(
                            f"State with ID '{state_id}' does not exist for City '{name}'."
                        )
                    )
                except ValueError as e:
                    self.stdout.write(
                        self.style.ERROR(f"Value error for City '{name}': {str(e)}")
                    )
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(
                            f"Error while processing City '{name}': {str(e)}"
                        )
                    )
