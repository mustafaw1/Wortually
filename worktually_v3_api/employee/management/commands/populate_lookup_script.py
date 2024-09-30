import os
import json
from django.core.management.base import BaseCommand
from employee.models import Permission


class Command(BaseCommand):
    help = "Populate Role model from JSON file"

    def handle(self, *args, **kwargs):
        filepath = os.path.join(
            "employee", "fixtures", "roles_permissions.json"
        )  # Path to your JSON file
        with open(filepath, "r") as file:
            data = json.load(file)
            for item in data:
                fields = item.get("fields")
                name = fields.get("name")
                # Create or get the Role
                role, created = Permission.objects.get_or_create(name=name)

        self.stdout.write(self.style.SUCCESS("Successfully populated Role model"))
