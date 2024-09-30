import os
import json
from django.core.management.base import BaseCommand
from job_seekers.models import JobTitle, JobTitleAssessment


class Command(BaseCommand):
    help = "Populate JobTitleAssessment model from JSON file"

    def handle(self, *args, **kwargs):
        file_path = os.path.join("lookups", "fixtures", "sample_questions.json")

        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

            job_title = JobTitle.objects.get(id=7)

            for item in data["questions"]:
                question = item.get("question")
                options = item.get("options")
                answer = item.get("answer")

                if question and options and answer:
                    JobTitleAssessment.objects.create(
                        job_title=job_title,
                        question=question,
                        options=options,
                        answer=answer,
                    )
                    self.stdout.write(
                        self.style.SUCCESS(f"Added assessment question: '{question}'")
                    )

        self.stdout.write(
            self.style.SUCCESS("Successfully populated job title assessments.")
        )
