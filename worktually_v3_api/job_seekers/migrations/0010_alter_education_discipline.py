# Generated by Django 5.0.6 on 2024-09-05 05:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("job_seekers", "0009_rename_title_jobprofileportfolio_project_title_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="education",
            name="discipline",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]