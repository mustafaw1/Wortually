# Generated by Django 5.0.6 on 2024-09-04 10:55

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("job_seekers", "0004_remove_jobprofile_job_profile_name"),
        ("lookups", "0007_degreetitle"),
    ]

    operations = [
        migrations.RenameField(
            model_name="education",
            old_name="completion_date",
            new_name="from_date",
        ),
        migrations.RemoveField(
            model_name="education",
            name="certificate_photo",
        ),
        migrations.RemoveField(
            model_name="education",
            name="education_type_id",
        ),
        migrations.RemoveField(
            model_name="education",
            name="major_subjects",
        ),
        migrations.RemoveField(
            model_name="education",
            name="score",
        ),
        migrations.RemoveField(
            model_name="education",
            name="title",
        ),
        migrations.AddField(
            model_name="education",
            name="created_at",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name="education",
            name="degree_type",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="educations",
                to="lookups.degreetype",
            ),
        ),
        migrations.AddField(
            model_name="education",
            name="discipline",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="educations",
                to="lookups.degreetitle",
            ),
        ),
        migrations.AddField(
            model_name="education",
            name="to_date",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="education",
            name="updated_at",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name="education",
            name="institute_name",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]