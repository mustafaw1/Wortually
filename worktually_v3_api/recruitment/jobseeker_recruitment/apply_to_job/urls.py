from django.urls import path
from .views import ApplyToJobView

urlpatterns = [
    path("apply-to-job/", ApplyToJobView.as_view(), name="apply-to-job"),
]
