from django.contrib import admin
from django.contrib import admin
from .models import (
    Employee,
    Education,
    Experience,
    Dependent,
    Invitation,
    Organization,
    Role,
    Role_has_Permission,
    Setting,
    Language,
    Location,
    Portfolio,
    OTP,
)

admin.site.register(Education)
admin.site.register(Experience)
admin.site.register(Dependent)
admin.site.register(Organization)
admin.site.register(Role)
admin.site.register(Role_has_Permission)
admin.site.register(Setting)
admin.site.register(Language)
admin.site.register(Location)
admin.site.register(Portfolio)
admin.site.register(Invitation)
admin.site.register(OTP)


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "email", "is_active", "is_staff")
    search_fields = ("first_name", "last_name", "email")
