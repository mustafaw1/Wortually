from django.http import JsonResponse
from recruitment.models import APIKey


def api_key_required(view_func):
    def wrapped_view(request, *args, **kwargs):
        api_key = request.headers.get("Authorization")
        try:
            api_key_object = APIKey.objects.get(key=api_key, is_active=True)
        except APIKey.DoesNotExist:
            return JsonResponse({"error": "Invalid API key"}, status=401)

        # Attach the API key object to request for further processing if needed
        request.api_key = api_key_object
        return view_func(request, *args, **kwargs)

    return wrapped_view
