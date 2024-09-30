from django.urls import path, include


urlpatterns = [
    path("api/", include("job_seekers.modules.accounts.urls")),
    path("api/job_seeker/", include("job_seekers.modules.job_seeker.urls")),
    path("api/job_profile/", include("job_seekers.modules.job_profiles.urls")),
    path("api/experience/", include("job_seekers.modules.experience.urls")),
    path("api/", include("job_seekers.modules.skills.urls")),
    path("api/", include("job_seekers.modules.job_assessment.urls")),
    path("api/", include("job_seekers.modules.job_interviews.urls")),
    path("api/education/", include("job_seekers.modules.education.urls")),
    path("api/language/", include("job_seekers.modules.languages.urls")),
]
