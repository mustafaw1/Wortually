from django.db import models
import secrets


class APIKey(models.Model):
    key = models.CharField(max_length=40, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = secrets.token_hex(20)  # Generate a random key
        super().save(*args, **kwargs)

    def __str__(self):
        return self.key
