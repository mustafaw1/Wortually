from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models
from django.db import transaction
import pytz
from lookups.models import City, Country, State, Source
from django.utils import timezone

class JobSeekerManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(
            email=email, first_name=first_name, last_name=last_name, **extra_fields
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


class JobSeeker(AbstractBaseUser):
   
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]

    AVAILABILITY_CHOICES = [
        ('available', 'Available'),
        ('not_available', 'Not Available'),
    ]

    email = models.EmailField(unique=True, max_length=255)
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    phone = models.CharField(max_length=45, blank=True)
    father_name = models.CharField(max_length=45, blank=True)
    source = models.ForeignKey(Source, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=45, blank=True, choices=AVAILABILITY_CHOICES)
    birth_date = models.DateField(null=True, blank=True)
    id_number = models.CharField(max_length=45, blank=True)
    marital_status = models.CharField(max_length=45, blank=True)
    gender = models.CharField(max_length=45, blank=True, choices=GENDER_CHOICES)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    profile_picture_url = models.URLField(max_length=500, blank=True, null=True)
    cover_photo = models.ImageField(upload_to='cover_photos/', blank=True, null=True)
    about = models.TextField(blank=True)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, blank=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True)
    state = models.ForeignKey(State, on_delete=models.SET_NULL, null=True, blank=True)

    created_at = models.DateTimeField(default=timezone.now)  
    updated_at = models.DateTimeField(auto_now=True)
    timezone = models.CharField(
        max_length=50,
        choices=[(tz, tz) for tz in pytz.all_timezones], 
        default='UTC',
        help_text="User's timezone"
    )


    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = JobSeekerManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    class Meta:
        indexes = [
            models.Index(fields=["id"]),
        ]
        app_label = "job_seekers"

    def get_current_time(self):
        """
        Get the current time in the user's timezone, or UTC if not set.
        """
        user_timezone = self.timezone if self.timezone else 'UTC'
        tz = pytz.timezone(user_timezone)
        return timezone.now().astimezone(tz)

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_short_name(self):
        return self.first_name

    def has_perm(self, perm, obj=None):
        return self.is_superuser or self.is_staff

    def has_module_perms(self, app_label):
        return self.is_superuser or self.is_staff

    def get_profile_completion(self):
        approval = ApprovalModel.objects.get(job_seeker=self)
        return approval.profile_completion_percentage

    def update_profile_completion(self):
        print(f"Updating profile completion for JobSeeker {self.id}")

        # Calculate profile picture URL points
        profile_picture_points = 1 if self.profile_picture_url else 0
        print(f"Profile picture URL points: {profile_picture_points}")

        # Calculate education points
        education_points = 1 if self.Education.exists() else 0
        print(f"Education points: {education_points}")

        # Calculate languages points
        languages_points = 1 if self.language.exists() else 0
        print(f"Languages points: {languages_points}")


        total_points = (
            + profile_picture_points
            + education_points
            + languages_points
           
        )
        profile_completion_percentage = (total_points / 4.25) * 100
        print(profile_completion_percentage)
        # Update or create ApprovalModel instance
        with transaction.atomic():
            approval, created = ApprovalModel.objects.get_or_create(job_seeker=self)
            approval.profile_completion_percentage = profile_completion_percentage
            approval.save()

    


class ApprovalModel(models.Model):
    job_seeker = models.OneToOneField('job_seekers.JobSeeker', on_delete=models.CASCADE, related_name="approval")
    profile_completion_percentage = models.FloatField(default=0)
    is_approved = models.BooleanField(default=False)

    class Meta:
        app_label = "job_seekers"

    def __str__(self):
        return f"Approval for {self.job_seeker.first_name} {self.job_seeker.last_name}"
