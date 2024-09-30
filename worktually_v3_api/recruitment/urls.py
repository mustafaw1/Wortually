from django.urls import path, include
from .views import (
    JobPostCreateView,
    JobPostEditView,
    JobPostDeleteView,
    JobPostDetailView,
    JobPostListView,
)

urlpatterns = [
    path("api/job-posts/add", JobPostCreateView.as_view(), name="job-post-create"),
    path(
        "api/job-posts/edit/<int:pk>/", JobPostEditView.as_view(), name="job-post-edit"
    ),
    path(
        "api/job-posts/delete/<int:pk>/",
        JobPostDeleteView.as_view(),
        name="job-post-delete",
    ),
    path(
        "api/job-posts/<int:pk>/", JobPostDetailView.as_view(), name="job-post-detail"
    ),
    path("api/job-posts/list/", JobPostListView.as_view(), name="job_post_list"),
    path("api/", include("recruitment.jobseeker_recruitment.job_search.urls")),
    path("api/", include("recruitment.jobseeker_recruitment.apply_to_job.urls")),
    path(
        "api/", include("recruitment.jobseeker_recruitment.accept_reject_joboffer.urls")
    ),
    path(
        "api/",
        include("recruitment.jobseeker_recruitment.accept_reject_interview.urls"),
    ),
    path(
        "api/", include("recruitment.organization_recruitment.search_candidates.urls")
    ),
    path(
        "api/",
        include("recruitment.organization_recruitment.send_interview_request.urls"),
    ),
    path(
        "api/", include("recruitment.organization_recruitment.shortlist_candidate.urls")
    ),
    path("api/", include("recruitment.organization_recruitment.send_joboffer.urls")),
    path("api/", include("recruitment.organization_recruitment.hire_candidate.urls")),
]
