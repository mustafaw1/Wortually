# Generated by Django 5.0.6 on 2024-09-11 12:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "job_seekers",
            "0025_rename_portfolio_images_jobprofileportfolio_portfolio_image",
        ),
    ]

    operations = [
        migrations.RemoveField(
            model_name="jobprofileportfolio",
            name="portfolio_image",
        ),
        migrations.AddField(
            model_name="jobprofileportfolio",
            name="image_url",
            field=models.URLField(blank=True, null=True),
        ),
    ]
