# Generated by Django 5.0.6 on 2024-08-12 07:11

import django.db.models.deletion
import django.db.models.fields
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Organization",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=45)),
                ("email", models.EmailField(max_length=45, unique=True)),
                ("phone", models.CharField(max_length=45)),
                ("country_id", models.IntegerField(blank=True, null=True)),
                ("website", models.URLField(blank=True, max_length=45, null=True)),
                ("logo", models.TextField(blank=True, null=True)),
                ("industry_id", models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="OTP",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("email", models.EmailField(max_length=254)),
                ("otp", models.CharField(max_length=6)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("is_verified", models.BooleanField(default=False)),
                ("reset_token", models.UUIDField(default=uuid.uuid4, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name="PermissionGroup",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name="Setting",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100, unique=True)),
                ("value", models.TextField()),
                (
                    "timezone",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("UTC", "Coordinated Universal Time"),
                            ("US/Eastern", "Eastern Time (US & Canada)"),
                            ("US/Central", "Central Time (US & Canada)"),
                        ],
                        max_length=50,
                        null=True,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Employee",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                ("first_name", models.CharField(blank=True, default="", max_length=30)),
                ("last_name", models.CharField(blank=True, default="", max_length=150)),
                ("password", models.CharField(default="", max_length=128)),
                (
                    "father_name",
                    models.CharField(blank=True, default="", max_length=100, null=True),
                ),
                ("email", models.EmailField(default="", max_length=254, unique=True)),
                ("phone", models.CharField(default="", max_length=45)),
                ("designation_id", models.IntegerField(null=True)),
                ("department_id", models.IntegerField(null=True)),
                ("date_of_birth", models.DateField(blank=True, null=True)),
                (
                    "id_number",
                    models.CharField(blank=True, default="", max_length=50, null=True),
                ),
                (
                    "marital_status",
                    models.CharField(default="unmarried", max_length=20),
                ),
                ("gender", models.CharField(default="", max_length=10)),
                ("address", models.TextField(blank=True, default="", null=True)),
                ("country", models.CharField(default="", max_length=100)),
                ("state", models.CharField(default="", max_length=100)),
                ("city", models.CharField(default="", max_length=100)),
                ("postal_code", models.CharField(default="", max_length=20)),
                ("location_id", models.CharField(default="", max_length=45)),
                (
                    "picture",
                    models.ImageField(
                        blank=True, null=True, upload_to="profile_pictures/"
                    ),
                ),
                (
                    "cover_photo",
                    models.ImageField(blank=True, null=True, upload_to="cover_photos/"),
                ),
                (
                    "social_insurance_number",
                    models.CharField(blank=True, default="", max_length=50, null=True),
                ),
                ("about", models.TextField(blank=True, default="", null=True)),
                (
                    "source_of_hiring",
                    models.CharField(blank=True, default="", max_length=100, null=True),
                ),
                ("date_of_joining", models.DateField(blank=True, null=True)),
                (
                    "employee_type",
                    models.CharField(blank=True, default="", max_length=50, null=True),
                ),
                ("exit_date", models.DateField(blank=True, null=True)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("Active", "Active"),
                            ("Resigned", "Resigned"),
                            ("Terminated", "Terminated"),
                            ("Suspended", "Suspended"),
                        ],
                        default="Active",
                        max_length=20,
                    ),
                ),
                ("is_active", models.BooleanField(default=True)),
                ("is_staff", models.BooleanField(default=False)),
                (
                    "reporting_to",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="subordinates",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="EmergencyContact",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=45)),
                ("email", models.EmailField(max_length=45)),
                ("phone", models.CharField(max_length=45)),
                ("relation", models.CharField(max_length=45)),
                ("address", models.TextField()),
                ("country_id", models.IntegerField(blank=True, null=True)),
                ("state_id", models.IntegerField(blank=True, null=True)),
                ("city_id", models.IntegerField(blank=True, null=True)),
                ("postal_code", models.CharField(max_length=45)),
                (
                    "employee",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="emergency_contacts",
                        to="employee.employee",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Education",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("degree_title", models.CharField(max_length=100)),
                ("degree_type", models.CharField(max_length=50)),
                ("score", models.CharField(max_length=20)),
                ("major_subjects", models.CharField(max_length=255)),
                ("date_of_completion", models.DateField()),
                ("institute_name", models.CharField(max_length=100)),
                (
                    "degree_certificate",
                    models.FileField(
                        blank=True, null=True, upload_to="degree_certificates/"
                    ),
                ),
                (
                    "employee",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="employee_educations",
                        to="employee.employee",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Dependent",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("relation", models.CharField(max_length=100)),
                ("id_number", models.CharField(blank=True, max_length=50, null=True)),
                (
                    "social_insurance_number",
                    models.CharField(blank=True, max_length=50, null=True),
                ),
                (
                    "employee_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="employee.employee",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="BankAccount",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("bank_name", models.CharField(max_length=45)),
                ("iban", models.CharField(max_length=45)),
                ("account_number", models.CharField(max_length=45)),
                ("currency", models.CharField(max_length=45)),
                (
                    "employee",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="bank_accounts",
                        to="employee.employee",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Experience",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("job_title", models.CharField(max_length=100)),
                ("company_name", models.CharField(max_length=100)),
                (
                    "job_type",
                    models.CharField(
                        choices=[
                            ("Full-time", "Full-time"),
                            ("Part-time", "Part-time"),
                            ("Contract", "Contract"),
                        ],
                        max_length=50,
                    ),
                ),
                ("start_date", models.DateField()),
                ("end_date", models.DateField(blank=True, null=True)),
                ("description", models.TextField(blank=True, null=True)),
                (
                    "experience_letter",
                    models.FileField(
                        blank=True, null=True, upload_to="experience_letters/"
                    ),
                ),
                (
                    "employee",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="experiences",
                        to="employee.employee",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Invitation",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("first_name", models.CharField(max_length=100)),
                ("last_name", models.CharField(max_length=100)),
                ("email", models.EmailField(max_length=254)),
                ("location", models.CharField(blank=True, max_length=100, null=True)),
                (
                    "salary_type",
                    models.CharField(
                        choices=[("Monthly", "Monthly"), ("Hourly", "Hourly")],
                        max_length=50,
                    ),
                ),
                ("salary", models.DecimalField(decimal_places=2, max_digits=10)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("Pending", "Pending"),
                            ("Accepted", "Accepted"),
                            ("Rejected", "Rejected"),
                        ],
                        default="Pending",
                        max_length=20,
                    ),
                ),
                (
                    "added_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="added_invitations",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "employee",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="invitations",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Language",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("language", models.CharField(max_length=100)),
                (
                    "level",
                    models.CharField(
                        choices=[
                            ("Basic", "Basic"),
                            ("Conversational", "Conversational"),
                            ("Fluent", "Fluent"),
                            ("Native", "Native"),
                        ],
                        max_length=50,
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="languages",
                        to="employee.employee",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Location",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=45)),
                ("default", models.BooleanField(default=False)),
                (
                    "organization",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="locations",
                        to="employee.organization",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Permission",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100, unique=True)),
                (
                    "permission_group",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="permissions",
                        to="employee.permissiongroup",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Portfolio",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=255)),
                ("url", models.URLField(blank=True, null=True)),
                (
                    "file",
                    models.FileField(
                        blank=True, null=True, upload_to="portfolio_files/"
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="portfolios",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Role",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100, unique=True)),
                (
                    "created_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="created_roles",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="employee",
            name="role",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.fields.SmallIntegerField,
                related_name="users",
                to="employee.role",
            ),
        ),
        migrations.CreateModel(
            name="Role_has_Permission",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "permission",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="role_permissions",
                        to="employee.permission",
                    ),
                ),
                (
                    "role",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="role_permissions",
                        to="employee.role",
                    ),
                ),
            ],
        ),
    ]