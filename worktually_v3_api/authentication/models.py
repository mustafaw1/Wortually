import random
import string
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
import uuid
from django.db import models

# class CustomUserManager(BaseUserManager):
#     def create_user(self, email, first_name, last_name, phone_number, password=None):
#         if not email:
#             raise ValueError('The Email field must be set')
#         user = self.model(
#             email=self.normalize_email(email),
#             first_name=first_name,
#             last_name=last_name,
#             phone_number=phone_number,
#         )
#         user.set_password(password)
#         user.save(using=self._db)
#         return user

#     def create_superuser(self, email, first_name, last_name, phone_number, password=None):
#         user = self.create_user(
#             email=email,
#             first_name=first_name,
#             last_name=last_name,
#             phone_number=phone_number,
#             password=password,
#         )
#         user.save(using=self._db)
#         return user

# class User(AbstractBaseUser):
#     email = models.EmailField(verbose_name='email', max_length=255, unique=True)
#     first_name = models.CharField(max_length=100)
#     last_name = models.CharField(max_length=100)
#     phone_number = models.CharField(max_length=15)
#     is_active = models.BooleanField(default=True)

#     objects = CustomUserManager()

#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['first_name', 'last_name', 'phone_number']

#     def __str__(self):
#         return self.email


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
