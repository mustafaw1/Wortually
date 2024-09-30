from django.core.management.base import BaseCommand
from job_seekers.models import Settings


class Command(BaseCommand):
    help = "Populates the Settings model with a key and a value of 3"

    def handle(self, *args, **kwargs):
        key_name = "profiles_limit"  # Set the key name
        value = "3"  # Set the value

        # Check if the key already exists
        if Settings.objects.filter(key=key_name).exists():
            self.stdout.write(
                self.style.WARNING(f'Settings with key "{key_name}" already exists.')
            )
        else:
            # Create the new setting
            setting = Settings.objects.create(key=key_name, value=value)
            self.stdout.write(
                self.style.SUCCESS(
                    f'Settings with key "{setting.key}" and value "{setting.value}" has been created.'
                )
            )
