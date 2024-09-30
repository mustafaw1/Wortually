from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import AccessToken
from employee.models import Employee
from job_seekers.models import JobSeeker


class JobSeekerJWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            return None

        token = auth_header.split(" ")[1]
        try:
            decoded_token = AccessToken(token)
            user_id = decoded_token.get("user_id")
            role = decoded_token.get("role")

            if role == "job_seeker":
                user = JobSeeker.objects.filter(pk=user_id).first()
                if not user:
                    raise AuthenticationFailed("No JobSeeker found with this ID.")
                return (user, token)
            else:
                raise AuthenticationFailed("Invalid token for JobSeeker endpoint.")
        except Exception as e:
            raise AuthenticationFailed("Token is invalid or expired.")


class EmployeeJWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            return None

        token = auth_header.split(" ")[1]
        try:
            decoded_token = AccessToken(token)
            user_id = decoded_token.get("user_id")
            role = decoded_token.get("role")

            if role == "employee":
                user = Employee.objects.filter(pk=user_id).first()
                if not user:
                    raise AuthenticationFailed("No Employee found with this ID.")
                return (user, token)
            else:
                raise AuthenticationFailed("Invalid token for Employee endpoint.")
        except Exception as e:
            raise AuthenticationFailed("Token is invalid or expired.")
