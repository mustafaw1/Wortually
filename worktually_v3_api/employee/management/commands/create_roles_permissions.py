from django.core.management.base import BaseCommand
from authentication.models import User  # Import your custom user model
from employee.models import Role, Permission, RolePermission, PermissionGroup


class Command(BaseCommand):
    def handle(self, *args, **options):
        # Create Permission Groups
        employees_group = PermissionGroup.objects.create(name="Employees")
        roles_group = PermissionGroup.objects.create(name="Roles")

        # Create Permissions
        employees_list = Permission.objects.create(
            permission_group=employees_group, name="Employees-List"
        )
        employees_view = Permission.objects.create(
            permission_group=employees_group, name="Employees-view"
        )
        employees_edit = Permission.objects.create(
            permission_group=employees_group, name="Employees-edit"
        )
        employees_delete = Permission.objects.create(
            permission_group=employees_group, name="Employees-delete"
        )

        roles_list = Permission.objects.create(
            permission_group=roles_group, name="Roles-List"
        )
        roles_view = Permission.objects.create(
            permission_group=roles_group, name="Roles-view"
        )
        roles_create = Permission.objects.create(
            permission_group=roles_group, name="Roles-create"
        )
        roles_edit = Permission.objects.create(
            permission_group=roles_group, name="Roles-edit"
        )
        roles_delete = Permission.objects.create(
            permission_group=roles_group, name="Roles-delete"
        )

        # Create Roles
        hr_manager = Role.objects.create(name="HR Manager")
        assistant_hr = Role.objects.create(name="Assistant HR")

        # Assign Permissions to Roles
        RolePermission.objects.create(role=hr_manager, permission=employees_list)
        RolePermission.objects.create(role=hr_manager, permission=employees_view)
        RolePermission.objects.create(role=hr_manager, permission=employees_edit)
        RolePermission.objects.create(role=hr_manager, permission=employees_delete)

        RolePermission.objects.create(role=assistant_hr, permission=employees_list)
        RolePermission.objects.create(role=assistant_hr, permission=employees_view)
        RolePermission.objects.create(role=assistant_hr, permission=employees_edit)
        RolePermission.objects.create(role=assistant_hr, permission=employees_delete)

        # Create Users and Assign Roles
        admin_user = User.objects.create_superuser(
            email="info@reachfirst.com",
            first_name="Admin",
            last_name="User",
            phone_number="0000000000",
            password="adminpassword",
        )
        hr_manager_user = User.objects.create_user(
            email="nafeesa@reachfirst.com",
            first_name="Nafeesa",
            last_name="HR",
            phone_number="0000000001",
            password="hrpassword",
        )
        assistant_hr_user = User.objects.create_user(
            email="anam@reachfirst.com",
            first_name="Anam",
            last_name="Assistant",
            phone_number="0000000002",
            password="assistantpassword",
        )

        admin_user.profile.role = (
            None  # Assuming admin has no specific role in your system
        )
        admin_user.profile.save()

        hr_manager_user.profile.role = hr_manager
        hr_manager_user.profile.save()

        assistant_hr_user.profile.role = assistant_hr
        assistant_hr_user.profile.save()

        print("Roles and permissions have been created and assigned.")
