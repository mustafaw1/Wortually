from datetime import timezone
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from job_seekers.modules.job_seeker.models import ApprovalModel
from django.db import transaction


class JobProfile(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", _("Pending")
        REJECTED = "rejected", _("Rejected")
        APPROVED = "approved", _("Approved")

    job_seeker = models.ForeignKey('job_seekers.JobSeeker', on_delete=models.CASCADE, related_name="job_profile")
    job_title = models.ForeignKey(
        "lookups.JobTitle",
        on_delete=models.CASCADE,
        null=True,
        default=None,
        related_name="job_profiles",
    )
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    completion_rate = models.IntegerField(default=0)
    priority = models.IntegerField(null=True, blank=True)
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.PENDING,
    )
    
    reviewed_at = models.CharField(max_length=45)
    rating = models.CharField(max_length=45)
    is_approved = models.BooleanField(default=False)

    class Meta:
        app_label = "job_seekers"

    def __str__(self):
        return f"Job Profile {self.id} - {self.job_title}"
    
    def update_profile_completion(self):
        print(f"Updating profile completion for JobProfile {self.id}")

        # Calculate experience points (1 point equals 23%)
        experience_points = 1 if self.jobprofile_experiences.exists() else 0
        print(f"Experience points: {experience_points}")

        # Calculate portfolio points (1 point equals 23%)
        portfolio_points = 1 if self.portfolios.exists() else 0
        print(f"Portfolio points: {portfolio_points}")

        # Calculate job profile skills points (1 point equals 23%)
        skills_points = 1 if self.job_profile_skills.exists() else 0
        print(f"Skills points: {skills_points}")

        # Fetch JobSeeker's completion rate from ApprovalModel
        try:
            approval = ApprovalModel.objects.get(job_seeker=self.job_seeker)
            job_seeker_completion_percentage = approval.profile_completion_percentage
            print(f"JobSeeker completion percentage: {job_seeker_completion_percentage}")
        except ApprovalModel.DoesNotExist:
            job_seeker_completion_percentage = 0  # Default to 0 if not found
            print("ApprovalModel not found for JobSeeker, defaulting to 0%")

        # Convert JobSeeker completion percentage to points (23% equals 1 point)
        job_seeker_completion_points = job_seeker_completion_percentage / 23
        print(f"JobSeeker completion points: {job_seeker_completion_points}")

        # Calculate total points
        total_points = (
            experience_points + portfolio_points + skills_points + job_seeker_completion_points
        )

         # Calculate completion rate based on 4 total points (100% max)
        self.completion_rate = min((total_points / 4) * 100, 100)  # Ensure it doesn't exceed 100%
        print(f"Final completion rate: {self.completion_rate}")



        # Update status based on completion rate
        if self.completion_rate >= 90:
            self.status = JobProfile.Status.APPROVED
        else:
            self.status = JobProfile.Status.PENDING

        self.save()





class JobProfileReview(models.Model):
    job_profile = models.ForeignKey(
        JobProfile, on_delete=models.CASCADE, related_name="reviews"
    )
    communication_rating = models.FloatField()
    experience_rating = models.FloatField()
    education_rating = models.FloatField()
    skills_rating = models.FloatField()
    comments = models.CharField(max_length=45)
    status = models.CharField(max_length=45)
    reject_reason_id = models.IntegerField()
    next_review = models.DateField()
    # reviewed_by = models.IntegerField()

    class Meta:
        app_label = "job_seekers"

    def __str__(self):
        return self.comments


class JobProfilePortfolio(models.Model):
    job_profile = models.ForeignKey(
        JobProfile, on_delete=models.CASCADE, related_name="portfolios"
    )
    project_title = models.CharField(max_length=45)
    description = models.TextField()
    url = models.CharField(max_length=255)
    image_url = models.URLField(max_length=200, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    class Meta:
        app_label = "job_seekers"

    def __str__(self):
        return self.project_title
