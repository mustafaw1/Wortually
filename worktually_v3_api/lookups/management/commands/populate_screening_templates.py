# job_seekers/management/commands/populate_screening_templates.py

import os
import json
from django.core.management.base import BaseCommand
from job_seekers.models import ScreeningInterviewTemplate, JobSeeker


class Command(BaseCommand):
    help = "Populate ScreeningInterviewTemplate model from JSON file"

    def handle(self, *args, **kwargs):
        file_path = os.path.join(
            "lookups", "fixtures", "interview_questions.json"
        )  # Update with your actual file path

        # Assuming the admin user's JobSeeker instance has an ID of 1
        admin_user_id = 1
        admin_user = JobSeeker.objects.get(id=admin_user_id)

        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

            for item in data:
                name = item.get("name")
                status = item.get("status")
                questions = item.get("questions")

                if name and status and questions:
                    ScreeningInterviewTemplate.objects.create(
                        name=name,
                        status=status,
                        questions=questions,
                        # added_by=admin_user,  # Assign the JobSeeker instance
                    )
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"Added screening interview template: '{name}'"
                        )
                    )

        self.stdout.write(
            self.style.SUCCESS("Successfully populated screening interview templates.")
        )
