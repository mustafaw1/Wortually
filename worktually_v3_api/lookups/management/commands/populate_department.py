import os
import json
from django.core.management.base import BaseCommand
from lookups.models import EmployeeType

class Command(BaseCommand):
    help = "Populates the EmployeeType model with data from a JSON file"

    def handle(self, *args, **kwargs):
        # Construct the file path
        file_path = os.path.join("lookups", "fixtures", "employee_type.json")

        # Open and read the JSON file
        with open(file_path, "r") as f:
            data = json.load(f)

        # Populate the EmployeeType model
        for item in data:
            employee_type, created = EmployeeType.objects.get_or_create(
                name=item["name"],
                defaults={"status": item["status"]}
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Added {employee_type.name} to EmployeeType table."))
            else:
                self.stdout.write(f"{employee_type.name} already exists.")

        self.stdout.write(self.style.SUCCESS("Successfully populated EmployeeType model."))
