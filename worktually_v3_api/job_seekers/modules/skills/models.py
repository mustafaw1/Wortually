from django.db import models
from job_seekers.models import JobProfile
from lookups.models import Skills


class JobProfileSkill(models.Model):
    skill = models.ForeignKey(
        Skills, on_delete=models.CASCADE, related_name="job_profile_skill"
    )
    job_profile = models.ForeignKey(
        JobProfile,
        on_delete=models.CASCADE,
        related_name="job_profile_skills",
        default="",
    )

    class Meta:
        app_label = "job_seekers"

    def __str__(self):
        return f"{self.skill.name} for profile {self.job_profile_id}"
