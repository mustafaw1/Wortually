from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


class Invitation(models.Model):
    employee = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="invitations"
    )
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    location = models.CharField(max_length=100, blank=True, null=True)
    salary_type = models.CharField(
        max_length=50, choices=[("Monthly", "Monthly"), ("Hourly", "Hourly")]
    )
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=20,
        choices=[
            ("Pending", "Pending"),
            ("Accepted", "Accepted"),
            ("Rejected", "Rejected"),
        ],
        default="Pending",
    )
    added_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="added_invitations",
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.email}"
