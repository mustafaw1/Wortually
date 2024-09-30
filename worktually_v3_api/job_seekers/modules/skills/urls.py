from django.urls import path
from job_seekers.modules.skills.views import *
from lookups.models import SkillCategory

urlpatterns = [
    path("category/add/", AddSkillCategoryView.as_view(), name="add_skill_category"),
    path(
        "category/update/<int:pk>/",
        UpdateSkillCategoryView.as_view(),
        name="update_skill_category",
    ),
    path(
        "category/delete/<int:pk>/",
        DeleteSkillCategoryView.as_view(),
        name="delete_skill_category",
    ),
    path('job_profile/update_skills/', UpdateJobProfileSkillsView.as_view(), name='update-job-profile-skills'),
]
