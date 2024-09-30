import os
import json
from django.core.management.base import BaseCommand
from lookups.models import (
    DegreeType,
)


class Command(BaseCommand):
    help = "Populate DegreeType model from JSON file"

    def handle(self, *args, **kwargs):
        file_path = os.path.join("lookups", "fixtures", "degree_subjects.json")

        with open(file_path, "r", encoding="utf-8") as file:
            degree_types_data = json.load(file)

            for degree_type_data in degree_types_data:
                name = degree_type_data.get("name")
                status = degree_type_data.get(
                    "status", "Active"
                )  # Default status if not provided

                if name:
                    try:
                        degree_type, created = DegreeType.objects.get_or_create(
                            name=name, status=status
                        )
                        if created:
                            self.stdout.write(
                                self.style.SUCCESS(
                                    f"DegreeType '{name}' added successfully"
                                )
                            )
                        else:
                            self.stdout.write(
                                self.style.SUCCESS(
                                    f"DegreeType '{name}' already exists"
                                )
                            )
                    except Exception as e:
                        self.stdout.write(
                            self.style.ERROR(
                                f"Error while processing DegreeType '{name}': {str(e)}"
                            )
                        )
                else:
                    self.stdout.write(
                        self.style.ERROR(
                            "Invalid DegreeType data: 'name' field is required"
                        )
                    )
