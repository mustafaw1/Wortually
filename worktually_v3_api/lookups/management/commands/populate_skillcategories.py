import os
import json
from django.core.management.base import BaseCommand
from lookups.models import SkillCategory


class Command(BaseCommand):
    help = "Populates the SkillCategory model with data from a JSON file"

    def handle(self, *args, **kwargs):
        # Construct the file path
        file_path = os.path.join("lookups", "fixtures", "skill_categories.json")

        # Open and read the JSON file
        with open(file_path, "r") as f:
            data = json.load(f)

        # Populate the SkillCategory model
        for item in data:
            SkillCategory.objects.get_or_create(name=item["name"])

        self.stdout.write(
            self.style.SUCCESS("Successfully populated SkillCategory model.")
        )
