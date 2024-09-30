from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse
from django.conf import settings
from recruitment.models import APIKey
import re


class APIKeyMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        # Define paths or views that require API key with regex for dynamic segments
        protected_paths = [
            r"^/api/recruitment/job-posts/$",
            r"^/api/recruitment/job-posts/list/$",
            r"^/api/organizations/$",
            r"^/api/interviews/\d+/accept-reject/$",
            r"^/api/interviews/\d+/reschedule/$",
        ]

        # Exact paths to exempt
        exempt_paths = [
            "/api/recruitment/job-posts/add",
            "/api/organizations/add",
            "/admin/login/",
        ]

        # Skip middleware for the exact exempt paths
        if request.path in exempt_paths:
            return None

        # Check if the request path requires an API key
        if any(re.fullmatch(path, request.path) for path in protected_paths):
            # Extract the API key from the 'Authorization' header
            authorization_header = request.headers.get("Authorization")

            if not authorization_header:
                return JsonResponse({"error": "API key required"}, status=401)

            if not authorization_header.startswith("Api-Key "):
                return JsonResponse({"error": "Invalid API key format"}, status=401)

            api_key = authorization_header[len("Api-Key ") :].strip()

            try:
                APIKey.objects.get(key=api_key, is_active=True)
            except APIKey.DoesNotExist:
                return JsonResponse({"error": "Invalid API key"}, status=401)

        # Continue processing the view
        return None
