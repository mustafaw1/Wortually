from django.db import models


class Industry(models.Model):
    name = models.CharField(max_length=100)
    status = models.CharField(max_length=50)

    class Meta:
        db_table = "lookup_industry"
        app_label = "lookups"


from django.db import models


class Country(models.Model):
    name = models.CharField(max_length=100, default="")
    iso3 = models.CharField(max_length=100, default="")
    iso2 = models.CharField(max_length=100, default="")
    phone_code = models.CharField(max_length=20, default="")
    capital = models.CharField(max_length=255, default="")
    currency = models.CharField(max_length=255, default="")

    def __str__(self):
        return self.name

    class Meta:
        db_table = "lookup_country"
        app_label = "lookups"


class State(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    state_code = models.CharField(max_length=10, default="", blank=True)

    class Meta:
        db_table = "lookup_state"
        app_label = "lookups"


class City(models.Model):
    name = models.CharField(max_length=100)
    state = models.ForeignKey("State", on_delete=models.CASCADE)
    country_id = models.IntegerField(null=True, blank=True)
    country_code = models.CharField(max_length=10, default="", blank=True)
    latitude = models.FloatField()
    longitude = models.FloatField()

    class Meta:
        db_table = "lookup_city"
        app_label = "lookups"


class Designation(models.Model):
    name = models.CharField(max_length=100)
    status = models.CharField(max_length=50)

    class Meta:
        db_table = "lookup_designation"
        app_label = "lookups"


class Department(models.Model):
    name = models.CharField(max_length=100)
    status = models.CharField(max_length=50)

    class Meta:
        db_table = "lookup_department"
        app_label = "lookups"


class JobTitle(models.Model):
    name = models.CharField(max_length=200)
    department = models.ForeignKey(
        Department, on_delete=models.CASCADE, related_name="job_titles"
    )

    def __str__(self):
        return self.name

    class Meta:
        indexes = [
            models.Index(fields=["id"]),
        ]
        app_label = "lookups"


class Source(models.Model):
    name = models.CharField(max_length=100)
    status = models.CharField(max_length=50)

    class Meta:
        db_table = "lookup_source"
        app_label = "lookups"


class DegreeType(models.Model):
    name = models.CharField(max_length=100)
    status = models.CharField(max_length=50)

    class Meta:
        db_table = "lookup_degree_type"
        app_label = "lookups"

class DegreeTitle(models.Model):
    name = models.CharField(max_length=255)
    active_status = models.BooleanField(default=True)
    degree_type = models.ForeignKey(DegreeType, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Degree'
        verbose_name_plural = 'Degrees'

class EmployeeType(models.Model):
    name = models.CharField(max_length=100)
    status = models.CharField(max_length=50)

    class Meta:
        db_table = "lookup_employee_type"
        app_label = "lookups"


class JobType(models.Model):
    name = models.CharField(max_length=100)
    status = models.CharField(max_length=50)

    class Meta:
        db_table = "lookup_job_type"
        app_label = "lookups"


class Relation(models.Model):
    name = models.CharField(max_length=100)
    status = models.CharField(max_length=50)

    class Meta:
        db_table = "lookup_relation"
        app_label = "lookups"


class SkillCategory(models.Model):
    name = models.CharField(max_length=45)
    deleted_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(null=True, auto_now_add=True)
    updated_at = models.DateTimeField(null=True, auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        app_label = "lookups"


class Skills(models.Model):
    skill_category = models.ForeignKey(
        SkillCategory, on_delete=models.CASCADE, related_name="skills"
    )
    name = models.CharField(max_length=45)
    deleted_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(null=True, auto_now_add=True)
    updated_at = models.DateTimeField(null=True, auto_now=True)

    class Meta:
        app_label = "lookups"

    def __str__(self):
        return self.name


class Language(models.Model):
    name = models.CharField(max_length=100)
    status = models.CharField(max_length=50)

    class Meta:
        db_table = "lookup_language"
        app_label = "lookups"


class DegreeSubject(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    

