from django.core.management.base import BaseCommand
from django.conf import settings
from rest_framework_simplejwt.tokens import AccessToken
from employee.models import Employee
from job_seekers.models import JobSeeker


class Command(BaseCommand):
    help = "Validate a JWT token and check the user ID and role in Employee or JobSeeker model"

    def add_arguments(self, parser):
        parser.add_argument("token", type=str)

    def handle(self, *args, **kwargs):
        token = kwargs["token"]

        self.stdout.write(f"Received token: {token}")

        try:
            # Decode the token
            decoded_token = AccessToken(token)

            # Extract the user ID and role
            user_id = decoded_token.get(settings.SIMPLE_JWT["USER_ID_CLAIM"])
            role = decoded_token.get("role")  # Extract the role

            # Debugging statements
            self.stdout.write(f"Decoded user ID: {user_id}")
            self.stdout.write(f"Decoded role: {role}")

            # Check if the user exists based on role
            if role == "employee":
                self.stdout.write("Checking Employee model...")
                try:
                    user = Employee.objects.get(id=user_id)
                    self.stdout.write(f"User found in Employee model: {user}")
                    self.stdout.write(
                        "Token is valid and contains the correct user ID and role."
                    )
                except Employee.DoesNotExist:
                    self.stdout.write(f"No employee found with ID: {user_id}")
                    self.stdout.write(
                        "Token is valid but does not contain a valid employee ID."
                    )
            elif role == "job_seeker":
                self.stdout.write("Checking JobSeeker model...")
                try:
                    user = JobSeeker.objects.get(id=user_id)
                    self.stdout.write(f"User found in JobSeeker model: {user}")
                    self.stdout.write(
                        "Token is valid and contains the correct user ID and role."
                    )
                except JobSeeker.DoesNotExist:
                    self.stdout.write(f"No job seeker found with ID: {user_id}")
                    self.stdout.write(
                        "Token is valid but does not contain a valid job seeker ID."
                    )
            else:
                self.stdout.write(f"Unknown role: {role}")

        except Exception as e:
            self.stdout.write(f"Token validation failed: {e}")
