from django.core.management.base import BaseCommand
from lookups.models import Skill as LookupSkill
from job_seekers.models import Skills, SkillCategory


class Command(BaseCommand):
    help = "Synchronize the Skill table with the lookups_skill table"

    def handle(self, *args, **kwargs):
        # Optional: Clear existing skills if you want to reset the table
        Skills.objects.all().delete()

        # Synchronize the skills
        for lookup_skill in LookupSkill.objects.all():
            skill_category, created = SkillCategory.objects.get_or_create(
                name="Default Category"
            )  # Adjust category as needed
            Skills.objects.create(skill_category=skill_category, name=lookup_skill.name)
            self.stdout.write(
                self.style.SUCCESS(f"Successfully added skill: {lookup_skill.name}")
            )

        self.stdout.write(self.style.SUCCESS("Successfully synchronized skills."))
