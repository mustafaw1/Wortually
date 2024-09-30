from django.db import models
from recruitment.organization_recruitment.API_keys.models import APIKey
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from job_seekers.models import JobProfile, JobSeeker
import requests
import os


class JobPost(models.Model):
    organization_id = models.IntegerField(null=True, blank=True)
    manager_id = models.IntegerField()
    job_title_id = models.IntegerField()
    job_type_id = models.IntegerField()
    description = models.TextField()
    slug = models.TextField()
    salary_type_id = models.IntegerField()
    amount = models.IntegerField()
    experience_required = models.IntegerField()
    education_required = models.TextField()
    skills = models.TextField()
    gender = models.CharField(max_length=45)
    status = models.CharField(max_length=45)
    closed_reason = models.TextField()
    expired_date = models.DateTimeField()
    shift_type_id = models.IntegerField()
    shift_start = models.DateTimeField()
    shift_end = models.DateTimeField()
    shift_hours = models.IntegerField()

    def __str__(self):
        return f"JobPost {self.id}: {self.description[:50]}..."


class JobInterview(models.Model):
    jobpost_id = models.ForeignKey(JobPost, on_delete=models.CASCADE)
    candidate_id = models.CharField(max_length=45)
    interview_method_id = models.IntegerField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    reschedule_start_date = models.DateTimeField(null=True, blank=True)
    reschedule_end_date = models.DateTimeField(null=True, blank=True)
    reschedule_by = models.CharField(max_length=45, null=True, blank=True)
    status = models.CharField(max_length=45)
    feedback = models.TextField()
    meeting_url = models.TextField()
    event_id = models.TextField()
    rating = models.TextField()
    expired_at = models.CharField(max_length=45)
    cancel_reason = models.TextField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"JobInterview {self.id} for JobPost {self.job_post_id}"


class JobOffer(models.Model):
    job_post_id = models.IntegerField()
    candidate_id = models.CharField(max_length=45)
    currency = models.CharField(max_length=45)
    amount = models.IntegerField()
    counter_amount = models.IntegerField()
    counter_by = models.TextField()
    status = models.CharField(max_length=45)
    rejected_reason = models.TextField()
    expired_at = models.CharField(max_length=45)

    def __str__(self):
        return f"JobOffer {self.id} for JobPost {self.job_post_id}"


class JobApplication(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", _("Pending")
        SHORTLISTED = "shortlisted", _("Shortlisted")
        REJECTED = "rejected", _("Rejected")

    job_id = models.IntegerField()
    job_seeker = models.ForeignKey(
        JobSeeker, on_delete=models.CASCADE, related_name="applications"
    )
    job_profile = models.ForeignKey(
        JobProfile, on_delete=models.CASCADE, related_name="applications"
    )
    date_applied = models.DateTimeField(default=timezone.now)
    source = models.CharField(max_length=255)
    is_applied = models.BooleanField(default=False)
    status = models.CharField(
        max_length=12,
        choices=Status.choices,
        default=Status.PENDING,
    )

    class Meta:
        app_label = "recruitment"


class Candidate(models.Model):
    job_application_id = models.ForeignKey(
        JobApplication, on_delete=models.CASCADE, related_name="job_applications"
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
