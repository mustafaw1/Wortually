# Generated by Django 5.0.6 on 2024-08-21 11:28

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("lookups", "0005_jobtitle"),
    ]

    operations = [
        migrations.CreateModel(
            name="DegreeSubject",
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
                ("name", models.CharField(max_length=255)),
            ],
        ),
    ]