from django.urls import path, include
from .views import AddEmployee
from .modules.education_experience.views import *
from .modules.skills_languages_portfolio.views import *
from .modules.dependents.views import *
from .modules.users.views import *
from .modules.accounts.views import *
from .modules.roles_permissions.views import (
    PermissionGroupsListView,
    AddPermissionGroupView,
    EditPermissionGroupView,
    PermissionGroupDetailView,
    AddPermissionsToGroupView,
    DeletePermissionsFromGroupView,
    DeletePermissionGroupView,
    RolesListView,
    AddRoleView,
    EditRoleView,
    DeleteRoleView,
    RoleDetailView,
    SyncPermissionsToRoleView,
    ViewPermissionGroup,
    EditPermissionsInGroup,
    AddPermissionsToRoleView,
    AddPermissionView,
)
from rest_framework.routers import DefaultRouter

router = DefaultRouter()


urlpatterns = [
    path(
        "employees/list",
        EmployeesListView.as_view(),
        name="employees-view",
        kwargs={"required_permission": "Employees-view"},
    ),
    path("employees/add/", AddEmployeeView.as_view(), name="add-employee"),
    path(
        "employees/<int:employee_id>/details",
        EmployeeDetailView.as_view(),
        name="employee-detail",
    ),
    path(
        "employees/edit-basic-information/<int:id>/",
        EditBasicInformationView.as_view(),
        name="edit-basic-info",
        kwargs={"required_permission": "Employees-edit"},
    ),
    path(
        "employees/<int:pk>/edit/work/",
        EditWorkInformationView.as_view(),
        name="edit-work-info",
        kwargs={"required_permission": "Employees-edit"},
    ),
    path(
        "employees/<int:pk>/edit/personal_info/",
        EditPersonalInformationView.as_view(),
        name="edit-personal-info",
        kwargs={"required_permission": "Employees-edit"},
    ),
    path(
        "employees/bank-accounts/add/",
        AddBankAccountView.as_view(),
        name="add-bank-account",
    ),
    path(
        "employees/emergency-contacts/add/",
        AddEmergencyContactView.as_view(),
        name="add-emergency-contact",
    ),
    path(
        "employees/<int:pk>/edit/bank_info/",
        EditBankAccountView.as_view(),
        name="edit-bank-account",
        kwargs={"required_permission": "Employees-edit"},
    ),
    path(
        "employees/<int:pk>/edit/emergency_info/",
        EditEmergencyInformationView.as_view(),
        name="edit-emergency-info",
        kwargs={"required_permission": "Employees-edit"},
    ),
    path(
        "employees/bank-accounts/<int:pk>/delete/",
        DeleteBankAccountView.as_view(),
        name="delete-bank-account",
    ),
    path(
        "employees/emergency-contacts/<int:pk>/delete/",
        DeleteEmergencyContactView.as_view(),
        name="delete-emergency-contact",
    ),
    path(
        "employees/<int:pk>/edit/profile-picture/",
        ChangeProfilePictureView.as_view(),
        name="change-profile-picture",
        kwargs={"required_permission": "Employees-edit"},
    ),
    path(
        "employees/<int:pk>/edit/cover-picture/",
        ChangeCoverPictureView.as_view(),
        name="change-cover-picture",
        kwargs={"required_permission": "Employees-edit"},
    ),
    path(
        "employees/experiences/list/",
        ExperiencesListView.as_view(),
        name="experiences-list",
        kwargs={"required_permission": "Employees-edit"},
    ),
    path(
        "employees/experience/add/",
        AddExperienceView.as_view(),
        name="add-experience",
        kwargs={"required_permission": "Employees-edit"},
    ),
    path(
        "employees/experiences/edit/<int:experience_id>/",
        EditExperienceView.as_view(),
        name="edit-experience",
        kwargs={"required_permission": "Employees-edit"},
    ),
    path(
        "employees/experiences/<int:experience_id>/delete/",
        DeleteExperienceView.as_view(),
        name="delete-experience",
        kwargs={"required_permission": "Employees-edit"},
    ),
    path(
        "employees/educations/list/",
        EducationsListView.as_view(),
        name="educations-list",
        kwargs={"required_permission": "Employees-edit"},
    ),
    path(
        "employees/educations/add/",
        AddEducationView.as_view(),
        name="add-education",
        kwargs={"required_permission": "Employees-edit"},
    ),
    path(
        "employees/educations/edit/<int:pk>/",
        EditEducationView.as_view(),
        name="edit-education",
        kwargs={"required_permission": "Employees-edit"},
    ),
    path(
        "employees/educations/<int:pk>/delete/",
        DeleteEducationView.as_view(),
        name="delete-education",
        kwargs={"required_permission": "Employees-edit"},
    ),
    path(
        "employees/dependents/list",
        DependentsListView.as_view(),
        name="dependents-list",
    ),
    path("employees/dependents/add/", AddDependentView.as_view(), name="add-dependent"),
    path(
        "employees/dependents/edit/<int:dependent_id>/",
        EditDependentView.as_view(),
        name="edit-dependent",
    ),
    path(
        "employees/dependents/<int:dependent_id>/delete/",
        DeleteDependentView.as_view(),
        name="delete-dependent",
    ),
    # path('employees/skills/list', SkillsListView.as_view(), name='skills-list'),
    # path('employees/skills/add/', AddSkillView.as_view(), name='add-skill'),
    # path('employees/skills/<int:skill_id>/delete/', DeleteSkillView.as_view(), name='delete-skill'),
    path(
        "employees/permission-groups/list",
        PermissionGroupsListView.as_view(),
        name="permission-groups-list",
    ),
    path(
        "employees/permission-groups/add/",
        AddPermissionGroupView.as_view(),
        name="add-permission-group",
    ),
    path(
        "employees/permission-groups/<int:group_id>/edit",
        EditPermissionGroupView.as_view(),
        name="edit-permission-group",
    ),
    path(
        "employees/permission-groups/<int:group_id>/detail/",
        PermissionGroupDetailView.as_view(),
        name="permission-group-detail",
    ),
    path(
        "employees/permission-groups/<int:group_id>/add-permissions/",
        AddPermissionsToGroupView.as_view(),
        name="add-permissions-to-group",
    ),
    path(
        "employees/permission-groups/<int:group_id>/",
        ViewPermissionGroup.as_view(),
        name="view-permission-group",
    ),
    path(
        "employees/permission-groups/<int:group_id>/edit-permissions/",
        EditPermissionsInGroup.as_view(),
        name="edit-permissions-in-group",
    ),
    path(
        "employees/permission-groups/<int:group_id>/delete-permissions/",
        DeletePermissionsFromGroupView.as_view(),
        name="delete-permissions-from-group",
    ),
    path(
        "employees/permission-groups/<int:group_id>/delete_permissions_group/",
        DeletePermissionGroupView.as_view(),
        name="delete-permission-group",
    ),
    path("permissions/add/", AddPermissionView.as_view(), name="add-permission"),
    path("employees/roles/list/", RolesListView.as_view(), name="roles-list"),
    path("employees/roles/add/", AddRoleView.as_view(), name="add-role"),
    path(
        "employees/roles/<int:role_id>/edit_role",
        EditRoleView.as_view(),
        name="edit-role",
    ),
    path(
        "employees/roles/<int:role_id>/delete/",
        DeleteRoleView.as_view(),
        name="delete-role",
    ),
    path(
        "employees/roles/<int:role_id>/detail/",
        RoleDetailView.as_view(),
        name="role-detail",
    ),
    path(
        "employees/roles/<int:role_id>/sync-permissions/",
        SyncPermissionsToRoleView.as_view(),
        name="sync-permissions-to-role",
    ),
    path(
        "roles/<int:role_id>/add-permissions/",
        AddPermissionsToRoleView.as_view(),
        name="add-permissions-to-role",
    ),
    path("", include("employee.modules.organization.urls")),
    path("", include("employee.modules.accounts.urls")),
]
