from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model
from employee.models import Employee
from job_seekers.models import JobSeeker


class EmployeeUserBackend(BaseBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        try:
            user = Employee.objects.get(email=email)
            if user.check_password(password):
                return user
        except Employee.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return Employee.objects.get(pk=user_id)
        except Employee.DoesNotExist:
            return None


class JobSeekerUserBackend(BaseBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        try:
            user = JobSeeker.objects.get(email=email)
            if user.check_password(password):
                return user
        except JobSeeker.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return JobSeeker.objects.get(pk=user_id)
        except JobSeeker.DoesNotExist:
            return None
