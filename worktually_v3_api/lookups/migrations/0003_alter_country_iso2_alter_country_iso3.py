# Generated by Django 5.0.6 on 2024-08-16 06:54

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("lookups", "0002_alter_country_iso2_alter_country_iso3"),
    ]

    operations = [
        migrations.AlterField(
            model_name="country",
            name="iso2",
            field=models.CharField(default="", max_length=100),
        ),
        migrations.AlterField(
            model_name="country",
            name="iso3",
            field=models.CharField(default="", max_length=100),
        ),
    ]
