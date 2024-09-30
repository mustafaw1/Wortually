# Generated by Django 5.0.6 on 2024-08-15 11:50

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("job_seekers", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="APIKey",
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
                ("key", models.CharField(max_length=40, unique=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("is_active", models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name="JobOffer",
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
                ("job_post_id", models.IntegerField()),
                ("candidate_id", models.CharField(max_length=45)),
                ("currency", models.CharField(max_length=45)),
                ("amount", models.IntegerField()),
                ("counter_amount", models.IntegerField()),
                ("counter_by", models.TextField()),
                ("status", models.CharField(max_length=45)),
                ("rejected_reason", models.TextField()),
                ("expired_at", models.CharField(max_length=45)),
            ],
        ),
        migrations.CreateModel(
            name="JobPost",
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
                ("organization_id", models.IntegerField(blank=True, null=True)),
                ("manager_id", models.IntegerField()),
                ("job_title_id", models.IntegerField()),
                ("job_type_id", models.IntegerField()),
                ("description", models.TextField()),
                ("slug", models.TextField()),
                ("salary_type_id", models.IntegerField()),
                ("amount", models.IntegerField()),
                ("experience_required", models.IntegerField()),
                ("education_required", models.TextField()),
                ("skills", models.TextField()),
                ("gender", models.CharField(max_length=45)),
                ("status", models.CharField(max_length=45)),
                ("closed_reason", models.TextField()),
                ("expired_date", models.DateTimeField()),
                ("shift_type_id", models.IntegerField()),
                ("shift_start", models.DateTimeField()),
                ("shift_end", models.DateTimeField()),
                ("shift_hours", models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name="JobApplication",
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
                ("job_id", models.IntegerField()),
                (
                    "date_applied",
                    models.DateTimeField(default=django.utils.timezone.now),
                ),
                ("source", models.CharField(max_length=255)),
                ("is_applied", models.BooleanField(default=False)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("pending", "Pending"),
                            ("shortlisted", "Shortlisted"),
                            ("rejected", "Rejected"),
                        ],
                        default="pending",
                        max_length=12,
                    ),
                ),
                (
                    "job_profile",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="applications",
                        to="job_seekers.jobprofile",
                    ),
                ),
                (
                    "job_seeker",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="applications",
                        to="job_seekers.jobseeker",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Candidate",
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
                ("status", models.CharField(max_length=45)),
                ("expected_start_date", models.DateField(blank=True, null=True)),
                (
                    "job_profile_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="candidates",
                        to="job_seekers.jobprofile",
                    ),
                ),
                (
                    "job_seeker_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="candidates",
                        to="job_seekers.jobseeker",
                    ),
                ),
                (
                    "job_application_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="job_applications",
                        to="recruitment.jobapplication",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="JobInterview",
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
                ("candidate_id", models.CharField(max_length=45)),
                ("interview_method_id", models.IntegerField()),
                ("start_date", models.DateTimeField()),
                ("end_date", models.DateTimeField()),
                ("reschedule_start_date", models.DateTimeField(blank=True, null=True)),
                ("reschedule_end_date", models.DateTimeField(blank=True, null=True)),
                (
                    "reschedule_by",
                    models.CharField(blank=True, max_length=45, null=True),
                ),
                ("status", models.CharField(max_length=45)),
                ("feedback", models.TextField()),
                ("meeting_url", models.TextField()),
                ("event_id", models.TextField()),
                ("rating", models.TextField()),
                ("expired_at", models.CharField(max_length=45)),
                (
                    "cancel_reason",
                    models.TextField(blank=True, max_length=100, null=True),
                ),
                (
                    "jobpost_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="recruitment.jobpost",
                    ),
                ),
            ],
        ),
    ]