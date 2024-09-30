from django.urls import path
from .views import *

urlpatterns = [
    path("add/", AddJobProfileView.as_view(), name="add_job_profile"),
    path("update/<int:pk>/", UpdateJobProfileView.as_view(), name="update_job_profile"),
    path("delete/<int:pk>/", DeleteJobProfileView.as_view(), name="delete_job_profile"),
    path("portfolio/add/", AddJobProfilePortfolioView.as_view(), name="add_portfolio"),
    path(
        "portfolio/update/<int:pk>/",
        UpdateJobProfilePortfolioView.as_view(),
        name="update_portfolio",
    ),
    path(
        "portfolio/delete/<int:pk>/",
        DeleteJobProfilePortfolioView.as_view(),
        name="delete_portfolio",
    ),
    path('info/', GetProfileInfo.as_view(), name='profile-info'),
    path(
        "job_profiles/<int:pk>/",
        JobProfileDetailView.as_view(),
        name="job_profile_detail",
    ),
]
