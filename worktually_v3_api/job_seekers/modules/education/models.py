from django.db import models
from django.apps import apps
from lookups.models import DegreeType, DegreeTitle
from django.utils import timezone


class Education(models.Model):
    job_seeker = models.ForeignKey(
        "job_seekers.JobSeeker", on_delete=models.CASCADE, related_name="Education"
    )
    degree_type = models.ForeignKey(
        DegreeType, on_delete=models.CASCADE, null=True,blank=True, related_name="educations"
    )
    discipline = models.CharField(max_length=100, null=True,blank=True)
    institute_name = models.CharField(max_length=100, null=True,blank=True,)
    from_date = models.DateField(null=True, blank=True)
    to_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    class Meta:
        app_label = "job_seekers"

    def __str__(self):
        return f"{self.degree_type} in {self.discipline} from {self.institute_name}"