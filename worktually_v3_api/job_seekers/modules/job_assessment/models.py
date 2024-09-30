from django.utils import timezone
from django.db import models
from lookups.models import Department
from lookups.models import JobTitle


class JobTitleAssessment(models.Model):
    job_title = models.ForeignKey(
        JobTitle, on_delete=models.CASCADE, related_name="assessments"
    )
    question = models.TextField()
    options = (
        models.JSONField()
    )  # Store options as a JSON string or comma-separated values
    answer = models.CharField(max_length=300)

    def __str__(self):
        return f"Assessment for {self.job_title.name}"

    class Meta:
        indexes = [
            models.Index(fields=["id"]),
        ]

    class Meta:
        app_label = "job_seekers"


class JobProfileAssessment(models.Model):
    job_profile = models.ForeignKey(
        "job_seekers.JobProfile", on_delete=models.CASCADE, related_name="assessments"
    )
    data = models.JSONField(default=None, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    obtained_marks = models.IntegerField(default=0)
    total_marks = models.IntegerField(default=26)
    status = models.CharField(max_length=45, default="Pending")

    def __str__(self):
        return f"Assessment for profile {self.job_profile.id}"

    class Meta:
        indexes = [
            models.Index(fields=["id"]),
        ]

    class Meta:
        app_label = "job_seekers"
