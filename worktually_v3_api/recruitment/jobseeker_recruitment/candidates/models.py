from django.db import models
from job_seekers.models import JobProfile, JobSeeker
from recruitment.models import JobApplications


class Candidate(models.Model):
    job_application_id = models.ForeignKey(
        JobApplications, on_delete=models.CASCADE, related_name="job_applications"
    )
    job_profile_id = models.ForeignKey(
        JobProfile, on_delete=models.CASCADE, related_name="candidates"
    )
    job_seeker_id = models.ForeignKey(
        JobSeeker, on_delete=models.CASCADE, related_name="candidates"
    )
    status = models.CharField(max_length=45)
    expected_start_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Candidate {self.id}"
