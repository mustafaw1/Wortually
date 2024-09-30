from django.db import models


class Setting(models.Model):
    name = models.CharField(max_length=100, unique=True)
    value = models.TextField()

    TIMEZONE_CHOICES = [
        ("UTC", "Coordinated Universal Time"),
        ("US/Eastern", "Eastern Time (US & Canada)"),
        ("US/Central", "Central Time (US & Canada)"),
        # Add more timezone choices as needed
    ]
    timezone = models.CharField(
        max_length=50, choices=TIMEZONE_CHOICES, null=True, blank=True
    )

    def __str__(self):
        return self.name
