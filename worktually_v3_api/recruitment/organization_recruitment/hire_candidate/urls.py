from django.urls import path
from .views import HireCandidateView

urlpatterns = [
    path("candidate/hire/", HireCandidateView.as_view(), name="hire_candidate"),
]
