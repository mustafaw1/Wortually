# your_app/decorators.py
from functools import wraps
from django.http import JsonResponse
from .models import APIKey


def api_key_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        # Extract the API key from the 'Authorization' header
        authorization_header = request.headers.get("Authorization", None)
        print(f"Authorization Header: {authorization_header}")  # Debug print

        if not authorization_header:
            return JsonResponse({"error": "API key required"}, status=401)

        if not authorization_header.startswith("Api-Key "):
            return JsonResponse({"error": "Invalid API key format"}, status=401)

        api_key = authorization_header.split("Api-Key ")[1].strip()

        try:
            APIKey.objects.get(key=api_key, is_active=True)
        except APIKey.DoesNotExist:
            return JsonResponse({"error": "Invalid API key"}, status=401)

        return view_func(request, *args, **kwargs)

    return _wrapped_view
