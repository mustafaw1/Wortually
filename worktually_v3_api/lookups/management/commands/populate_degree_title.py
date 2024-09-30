import os
import json
from django.core.management.base import BaseCommand
from job_seekers.models import JobTitle
from lookups.models import DegreeType


class Command(BaseCommand):
    help = "Populate JobTitle model from JSON file"

    def handle(self, *args, **kwargs):
        file_path = os.path.join("lookups", "fixtures", "degree_titles.json")

        with open(file_path, "r", encoding="utf-8") as file:
            job_titles_data = json.load(file)

            for job_title_data in job_titles_data:
                job_title_id = job_title_data.get("id")
                name = job_title_data.get("name")
                degree_type_id = job_title_data.get(
                    "degree_type_id"
                )  # Fetch degree_type_id from JSON data

                if job_title_id and name:
                    try:
                        degree_type = DegreeType.objects.get(id=degree_type_id)
                    except DegreeType.DoesNotExist:
                        self.stdout.write(
                            self.style.ERROR(
                                f"DegreeType with id '{degree_type_id}' does not exist. Skipping job title '{name}'"
                            )
                        )
                        continue

                    try:
                        job_title, created = JobTitle.objects.update_or_create(
                            id=job_title_id,
                            defaults={
                                "name": name,
                                "degree_type": degree_type,
                            },
                        )
                        if created:
                            self.stdout.write(
                                self.style.SUCCESS(
                                    f"JobTitle '{name}' added successfully"
                                )
                            )
                        else:
                            self.stdout.write(
                                self.style.SUCCESS(
                                    f"JobTitle '{name}' updated successfully"
                                )
                            )
                    except Exception as e:
                        self.stdout.write(
                            self.style.ERROR(
                                f"Error while processing JobTitle '{name}': {str(e)}"
                            )
                        )
                else:
                    self.stdout.write(
                        self.style.ERROR(
                            "Invalid JobTitle data: 'id' and 'name' fields are required"
                        )
                    )
