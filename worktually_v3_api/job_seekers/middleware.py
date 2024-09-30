import re
from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse
from job_seekers.models import APIKey


class APIKeyMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        # Define regex patterns for paths that require API key
        protected_paths = [
            r"^/api/candidates/.*$",
            r"^/api/job_profiles/.*$",
            r"^/api/job_seeker/list/\d+/$",
        ]

        # Define regex patterns for exempt paths if any
        exempt_paths = [
            r"^/api/recruitment/candidates/list$",
        ]

        # Function to check if a path matches any regex pattern
        def path_matches_patterns(path, patterns):
            for pattern in patterns:
                if re.match(pattern, path):
                    return True
            return False

        # Skip middleware for exempt paths
        if path_matches_patterns(request.path, exempt_paths):
            return None

        # Check if the request path requires an API key
        if path_matches_patterns(request.path, protected_paths):
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
