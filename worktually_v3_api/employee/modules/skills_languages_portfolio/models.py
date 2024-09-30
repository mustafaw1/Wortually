from django.db import models
from django.conf import settings
from employee.models import Employee


class Language(models.Model):
    user = models.ForeignKey(
        Employee, on_delete=models.CASCADE, related_name="languages"
    )
    language = models.CharField(max_length=100)
    level = models.CharField(
        max_length=50,
        choices=[
            ("Basic", "Basic"),
            ("Conversational", "Conversational"),
            ("Fluent", "Fluent"),
            ("Native", "Native"),
        ],
    )

    def __str__(self):
        return f"{self.language} ({self.level})"


class Portfolio(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="portfolios"
    )
    title = models.CharField(max_length=255)
    url = models.URLField(blank=True, null=True)
    file = models.FileField(upload_to="portfolio_files/", blank=True, null=True)

    def __str__(self):
        return f"{self.title}"
