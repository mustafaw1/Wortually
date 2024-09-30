import os
import json
from django.core.management.base import BaseCommand
from lookups.models import Skills, SkillCategory


class Command(BaseCommand):
    help = "Populates the Skills model with data from a JSON file"

    def handle(self, *args, **kwargs):
        # Construct the file path
        file_path = os.path.join("lookups", "fixtures", "technical_writing.json")

        # Open and read the JSON file
        with open(file_path, "r") as f:
            data = json.load(f)

        # Populate the Skills model
        for item in data:
            try:
                category = SkillCategory.objects.get(id=item["category_id"])
                Skills.objects.get_or_create(name=item["name"], skill_category=category)
            except SkillCategory.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(
                        f"SkillCategory with id {item['category_id']} does not exist."
                    )
                )

        self.stdout.write(self.style.SUCCESS("Successfully populated Skills model."))
