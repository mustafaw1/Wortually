from django.db import models
from django.conf import settings


class ScreeningInterviewTemplate(models.Model):
    name = models.CharField(max_length=45)
    status = models.CharField(max_length=45)
    questions = models.TextField()
    # added_by = models.ForeignKey(
    #     settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=None
    # )

    def __str__(self):
        return self.name

    class Meta:
        indexes = [
            models.Index(fields=["id"]),
        ]

    class Meta:
        app_label = "job_seekers"


class JobProfileInterview(models.Model):
    job_profile = models.ForeignKey("job_seekers.JobProfile", on_delete=models.CASCADE)
    interview_recording_url = models.CharField(max_length=45)
    result = models.CharField(max_length=45)
    transcription = models.TextField()
    status = models.CharField(max_length=45)
    screening_interview_template = models.ForeignKey(
        ScreeningInterviewTemplate, on_delete=models.CASCADE
    )

    def __str__(self):
        return f"Interview for {self.job_profile}"

    class Meta:
        app_label = "job_seekers"
