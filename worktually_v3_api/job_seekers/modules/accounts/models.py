import uuid
import random
import string
from django.db import models


class OTP(models.Model):
    email = models.EmailField()
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)
    reset_token = models.UUIDField(default=uuid.uuid4, unique=True)

    @staticmethod
    def generate_otp():
        return "".join(random.choices(string.digits, k=6))

    def __str__(self):
        return f"{self.email} - {self.otp}"

    class Meta:
        app_label = "job_seekers"
