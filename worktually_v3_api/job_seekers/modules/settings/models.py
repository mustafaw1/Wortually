from django.db import models


class Settings(models.Model):
    key = models.CharField(max_length=255, unique=True)
    value = models.CharField(max_length=255)

    class Meta:
        app_label = "job_seekers"

    def __str__(self):
        return self.key
