# Generated by Django 5.0.6 on 2024-09-12 06:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("job_seekers", "0027_jobseeker_created_at_jobseeker_timezone_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="jobprofile",
            name="completion_rate",
            field=models.IntegerField(default=0),
        ),
    ]
