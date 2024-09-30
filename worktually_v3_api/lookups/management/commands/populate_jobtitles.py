import os
import json
from django.core.management.base import BaseCommand
from lookups.models import SoftSkills, SkillCategory

class Command(BaseCommand):
    help = "Populates the SoftSkills model with data from a JSON file"

    def handle(self, *args, **kwargs):
        # Construct the file path
        file_path = os.path.join("lookups", "fixtures", "soft_skills.json")

        # Open and read the JSON file
        with open(file_path, "r") as f:
            data = json.load(f)

        # Populate the SoftSkills model
        for item in data:
            # Fetch the SkillCategory instance
            category = SkillCategory.objects.get(id=item["category_id"])

            # Create or get the SoftSkills instance
            SoftSkills.objects.get_or_create(
                name=item["name"],
                category=category
            )

        self.stdout.write(self.style.SUCCESS("Successfully populated SoftSkills model."))
