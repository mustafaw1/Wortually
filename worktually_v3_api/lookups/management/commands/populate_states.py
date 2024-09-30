from django.core.management.base import BaseCommand
from lookups.models import Country, State
import os
import json


class Command(BaseCommand):
    help = "Populates the State model with initial data"

    def handle(self, *args, **kwargs):
        # Correct file path
        file_path = os.path.join("lookups", "fixtures", "states.json")

        if not os.path.exists(file_path):
            self.stdout.write(self.style.ERROR(f"File not found: {file_path}"))
            return

        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        for state_data in data:
            state_id = state_data.get("id")
            name = state_data.get("name")
            country_id = state_data.get("country_id")
            state_code = state_data.get("state_code")

            try:
                country = Country.objects.get(id=country_id)
            except Country.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f"Country not found with ID: {country_id}")
                )
                continue

            state, created = State.objects.get_or_create(
                id=state_id,
                name=name,
                country=country,
                defaults={"state_code": state_code},
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f"Successfully added state: {name}")
                )
            else:
                self.stdout.write(self.style.WARNING(f"State already exists: {name}"))

        self.stdout.write(self.style.SUCCESS("State population completed."))
