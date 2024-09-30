from django.core.management.base import BaseCommand
from employee.models import Role, Permission, Role_has_Permission, PermissionGroup


class Command(BaseCommand):
    help = "Assigns permissions to roles"

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS("Starting to add permissions to roles..."))

        # Define your permissions and roles here
        permissions_to_roles = {
            "HR Manager": ["Employees-List", "Employees-view", "Employees-edit"],
            # Add more roles and permissions as needed
        }

        for role_name, permissions in permissions_to_roles.items():
            role, created = Role.objects.get_or_create(name=role_name)
            for permission_name in permissions:
                permission, perm_created = Permission.objects.get_or_create(
                    name=permission_name
                )

                # Get or create the PermissionGroup for the permission
                permission_group, group_created = PermissionGroup.objects.get_or_create(
                    name=permission_name
                )
                permission_group.permissions.add(permission)

                Role_has_Permission.objects.get_or_create(
                    role=role, permission=permission
                )

                if perm_created:
                    self.stdout.write(
                        self.style.SUCCESS(f"Created permission: {permission_name}")
                    )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created role: {role_name}"))

        self.stdout.write(
            self.style.SUCCESS("Permissions successfully added to roles.")
        )
