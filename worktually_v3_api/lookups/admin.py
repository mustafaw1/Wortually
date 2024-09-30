from django.contrib import admin
from .models import (
    Industry,
    Country,
    State,
    City,
    Designation,
    Department,
    JobTitle,
    Source,
    DegreeType,
    DegreeTitle,
    EmployeeType,
    JobType,
    Relation,
    SkillCategory,
    Skills,
    Language,
    DegreeSubject,
)

class IndustryAdmin(admin.ModelAdmin):
    list_display = ("name", "status")
    search_fields = ("name", "status")

class CountryAdmin(admin.ModelAdmin):
    list_display = ("name", "iso3", "iso2", "phone_code", "capital", "currency")
    search_fields = ("name", "iso3", "iso2", "phone_code", "capital", "currency")

class StateAdmin(admin.ModelAdmin):
    list_display = ("name", "country", "state_code")
    search_fields = ("name", "country__name", "state_code")

class CityAdmin(admin.ModelAdmin):
    list_display = ("name", "state", "country_id", "country_code", "latitude", "longitude")
    search_fields = ("name", "state__name", "country_id", "country_code")

class DesignationAdmin(admin.ModelAdmin):
    list_display = ("name", "status")
    search_fields = ("name", "status")

class DepartmentAdmin(admin.ModelAdmin):
    list_display = ("name", "status")
    search_fields = ("name", "status")

class JobTitleAdmin(admin.ModelAdmin):
    list_display = ("name", "department")
    search_fields = ("name", "department__name")

class SourceAdmin(admin.ModelAdmin):
    list_display = ("name", "status")
    search_fields = ("name", "status")

class DegreeTypeAdmin(admin.ModelAdmin):
    list_display = ("name", "status")
    search_fields = ("name", "status")

class DegreeTitleAdmin(admin.ModelAdmin):
    list_display = ("name", "degree_type", "active_status")
    search_fields = ("name", "degree_type__name")

class EmployeeTypeAdmin(admin.ModelAdmin):
    list_display = ("name", "status")
    search_fields = ("name", "status")

class JobTypeAdmin(admin.ModelAdmin):
    list_display = ("name", "status")
    search_fields = ("name", "status")

class RelationAdmin(admin.ModelAdmin):
    list_display = ("name", "status")
    search_fields = ("name", "status")

class SkillCategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)

class SkillsAdmin(admin.ModelAdmin):
    list_display = ("name", "skill_category")
    search_fields = ("name", "skill_category__name")

class LanguageAdmin(admin.ModelAdmin):
    list_display = ("name", "status")
    search_fields = ("name", "status")

class DegreeSubjectAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)

# Registering models with admin site
admin.site.register(Industry, IndustryAdmin)
admin.site.register(Country, CountryAdmin)
admin.site.register(State, StateAdmin)
admin.site.register(City, CityAdmin)
admin.site.register(Designation, DesignationAdmin)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(Source, SourceAdmin)
admin.site.register(DegreeType, DegreeTypeAdmin)
admin.site.register(DegreeTitle, DegreeTitleAdmin)
admin.site.register(EmployeeType, EmployeeTypeAdmin)
admin.site.register(JobType, JobTypeAdmin)
admin.site.register(Relation, RelationAdmin)
admin.site.register(SkillCategory, SkillCategoryAdmin)
admin.site.register(Skills, SkillsAdmin)
admin.site.register(Language, LanguageAdmin)
admin.site.register(DegreeSubject, DegreeSubjectAdmin)
