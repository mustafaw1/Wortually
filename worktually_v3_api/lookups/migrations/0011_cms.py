# Generated by Django 5.0.6 on 2024-09-16 07:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("lookups", "0010_advertisingtools"),
    ]

    operations = [
        migrations.CreateModel(
            name="CMS",
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
                (
                    "category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="cms",
                        to="lookups.skillcategory",
                    ),
                ),
            ],
            options={
                "indexes": [
                    models.Index(fields=["id"], name="lookups_cms_id_58a746_idx")
                ],
            },
        ),
    ]