from django.urls import path
from job_seekers.modules.experience.views import (
    AddExperienceView,
    UpdateExperienceView,
    DeleteExperienceView,
)

urlpatterns = [
    path("add/", AddExperienceView.as_view(), name="add_experience"),
    path("update/<int:experience_id>/", UpdateExperienceView.as_view(), name="update_experience"),
    path("delete/<int:experience_id>/", DeleteExperienceView.as_view(), name="delete_experience"),
]

