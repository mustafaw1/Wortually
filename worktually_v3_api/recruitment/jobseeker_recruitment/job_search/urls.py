from django.urls import path
from .views import JobSearchView

urlpatterns = [
    path("job-search/", JobSearchView.as_view(), name="job_search"),
]
