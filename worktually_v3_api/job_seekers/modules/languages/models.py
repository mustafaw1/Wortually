from django.db import models
from django.utils import timezone
from lookups.models import Language as LookupLanguage

class Language(models.Model):
    job_seeker = models.ForeignKey(
        "job_seekers.JobSeeker", on_delete=models.CASCADE, related_name="language"
    )
    language = models.ForeignKey(
        LookupLanguage, on_delete=models.CASCADE, null=True, related_name="job_seeker_languages"
    )
    PROFICIENCY_CHOICES = [
        ('Beginner', 'Beginner'),
        ('Intermediate', 'Intermediate'),
        ('Professional', 'Professional'),
    ]
    proficiency = models.CharField(max_length=45, null=True, choices=PROFICIENCY_CHOICES)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    class Meta:
        app_label = "job_seekers"

    def __str__(self):
        if self.language:  # Check if language is not None
            return f"{self.language.name} ({self.proficiency})"
        else:
            return f"Unknown Language ({self.proficiency})"

