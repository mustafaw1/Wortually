from django.db import models


class Organization(models.Model):
    name = models.CharField(max_length=45)
    email = models.EmailField(max_length=45, unique=True)
    phone = models.CharField(max_length=45)
    country_id = models.IntegerField(null=True, blank=True)
    website = models.URLField(max_length=45, blank=True, null=True)
    logo = models.TextField(blank=True, null=True)
    industry_id = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name


class Location(models.Model):
    name = models.CharField(max_length=45)
    default = models.BooleanField(default=False)
    organization = models.ForeignKey(
        Organization, related_name="locations", on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name
