from django.db import models
from django.conf import settings
from employee.models import Employee


class PermissionGroup(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Permission(models.Model):
    permission_group = models.ForeignKey(
        PermissionGroup, on_delete=models.CASCADE, related_name="permissions"
    )
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Role(models.Model):
    name = models.CharField(max_length=100, unique=True)
    created_by = models.ForeignKey(
        Employee,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_roles",
    )

    def __str__(self):
        return self.name


class Role_has_Permission(models.Model):
    role = models.ForeignKey(
        Role, on_delete=models.CASCADE, related_name="role_permissions"
    )
    permission = models.ForeignKey(
        Permission, on_delete=models.CASCADE, related_name="role_permissions"
    )

    def __str__(self):
        return f"{self.role.name} - {self.permission.name}"
