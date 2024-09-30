from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
import uuid
import random
import string


class EmployeeManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None):
        if not email:
            raise ValueError("The Email field must be set")
        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password=None):
        user = self.create_user(
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password,
        )
        user.save(using=self._db)
        return user


class Employee(AbstractBaseUser):
    first_name = models.CharField(max_length=30, blank=True, null=False, default="")
    last_name = models.CharField(max_length=150, blank=True, null=False, default="")
    password = models.CharField(max_length=128, null=False, default="")
    father_name = models.CharField(max_length=100, blank=True, null=True, default="")
    email = models.EmailField(blank=False, null=False, default="", unique=True)
    phone = models.CharField(max_length=45, null=False, default="")
    designation_id = models.IntegerField(null=True)
    department_id = models.IntegerField(null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    id_number = models.CharField(max_length=50, blank=True, null=True, default="")
    marital_status = models.CharField(
        max_length=20, blank=False, null=False, default="unmarried"
    )
    gender = models.CharField(max_length=10, blank=False, null=False, default="")
    address = models.TextField(blank=True, null=True, default="")
    country = models.CharField(max_length=100, blank=False, null=False, default="")
    state = models.CharField(max_length=100, blank=False, null=False, default="")
    city = models.CharField(max_length=100, blank=False, null=False, default="")
    postal_code = models.CharField(max_length=20, blank=False, null=False, default="")
    location_id = models.CharField(max_length=45, null=False, default="")
    picture = models.ImageField(upload_to="profile_pictures/", blank=True, null=True)
    cover_photo = models.ImageField(upload_to="cover_photos/", blank=True, null=True)
    social_insurance_number = models.CharField(
        max_length=50, blank=True, null=True, default=""
    )
    about = models.TextField(blank=True, null=True, default="")
    reporting_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="subordinates",
    )
    role = models.ForeignKey(
        "Role",
        on_delete=models.SmallIntegerField,
        null=True,
        blank=False,
        related_name="users",
    )
    source_of_hiring = models.CharField(
        max_length=100, blank=True, null=True, default=""
    )
    date_of_joining = models.DateField(blank=True, null=True)
    employee_type = models.CharField(max_length=50, blank=True, null=True, default="")
    exit_date = models.DateField(blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ("Active", "Active"),
            ("Resigned", "Resigned"),
            ("Terminated", "Terminated"),
            ("Suspended", "Suspended"),
        ],
        default="Active",
    )

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = EmployeeManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    def __str__(self):
        return self.email

    @property
    def is_anonymous(self):
        return False

    @property
    def is_authenticated(self):
        return True


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


class BankAccount(models.Model):
    employee = models.ForeignKey(
        Employee, on_delete=models.CASCADE, related_name="bank_accounts"
    )
    bank_name = models.CharField(max_length=45, null=False, blank=False)
    iban = models.CharField(max_length=45, null=False)
    account_number = models.CharField(max_length=45, null=False)
    currency = models.CharField(max_length=45, null=False)

    def __str__(self):
        return f"{self.bank_name} - {self.account_number}"


class EmergencyContact(models.Model):
    employee = models.ForeignKey(
        Employee, on_delete=models.CASCADE, related_name="emergency_contacts"
    )
    name = models.CharField(max_length=45)
    email = models.EmailField(max_length=45)
    phone = models.CharField(max_length=45)
    relation = models.CharField(max_length=45)
    address = models.TextField()
    country_id = models.IntegerField(null=True, blank=True)
    state_id = models.IntegerField(null=True, blank=True)
    city_id = models.IntegerField(null=True, blank=True)
    postal_code = models.CharField(max_length=45)

    def __str__(self):
        return f"{self.name} - {self.relation}"
