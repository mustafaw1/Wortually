from django.http import JsonResponse
from .task import add


def test_celery(request):
    result = add.delay(4, 6)
    return JsonResponse({"result": result.get()})
