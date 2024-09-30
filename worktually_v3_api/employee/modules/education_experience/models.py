from django.db import models
from employee.models import Employee


class Education(models.Model):
    employee = models.ForeignKey(
        Employee, on_delete=models.CASCADE, related_name="employee_educations"
    )
    degree_title = models.CharField(max_length=100)
    degree_type = models.CharField(max_length=50)
    score = models.CharField(max_length=20)
    major_subjects = models.CharField(max_length=255)
    date_of_completion = models.DateField()
    institute_name = models.CharField(max_length=100)
    degree_certificate = models.FileField(
        upload_to="degree_certificates/", blank=True, null=True
    )

    def __str__(self):
        return f"{self.degree_title} from {self.institute_name}"


class Experience(models.Model):
    employee = models.ForeignKey(
        Employee, on_delete=models.CASCADE, related_name="experiences"
    )
    job_title = models.CharField(max_length=100)
    company_name = models.CharField(max_length=100)
    job_type = models.CharField(
        max_length=50,
        choices=[
            ("Full-time", "Full-time"),
            ("Part-time", "Part-time"),
            ("Contract", "Contract"),
        ],
    )
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    experience_letter = models.FileField(
        upload_to="experience_letters/", blank=True, null=True
    )

    def __str__(self):
        return f"{self.job_title} at {self.company_name}"
