from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import PermissionGroup, Permission
from .serializers import PermissionGroupSerializer, PermissionSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.shortcuts import get_object_or_404
from .models import PermissionGroup, Permission, Role, Role_has_Permission
from .serializers import (
    PermissionGroupSerializer,
    PermissionSerializer,
    RoleSerializer,
    SyncPermissionsSerializer,
)
from django.conf import settings
from rest_framework.pagination import PageNumberPagination
from worktually_v3_api.custom_jwt.jwt import EmployeeJWTAuthentication


class PermissionGroupsListView(APIView):
    authentication_classes = [EmployeeJWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Get a list of all permission groups",
        responses={200: PermissionGroupSerializer(many=True)},
    )
    def get(self, request, *args, **kwargs):
        # Retrieve all permission groups
        groups = PermissionGroup.objects.all()

        paginator = PageNumberPagination()
        paginator.page_size = settings.REST_FRAMEWORK["PAGE_SIZE"]

        # Paginate the queryset
        paginated_groups = paginator.paginate_queryset(groups, request)

        # Serialize paginated data
        serializer = PermissionGroupSerializer(paginated_groups, many=True)

        # Return paginated response
        return paginator.get_paginated_response(serializer.data)


class ViewPermissionGroup(APIView):
    authentication_classes = [EmployeeJWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Get details of a specific permission group",
        responses={200: PermissionGroupSerializer()},
    )
    def get(self, request, group_id):
        permission_group = get_object_or_404(PermissionGroup, id=group_id)
        serializer = PermissionGroupSerializer(permission_group)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AddPermissionGroupView(APIView):
    authentication_classes = [EmployeeJWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Add a new permission group",
        request_body=PermissionGroupSerializer,
        responses={
            201: openapi.Response(
                "Permission group added successfully", PermissionGroupSerializer
            ),
            400: "Bad Request",
        },
        examples={
            "application/json": {
                "name": "Group Name",
            }
        },
    )
    def post(self, request):
        serializer = PermissionGroupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "message": "Permission group added successfully.",
                    "data": serializer.data,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AddPermissionView(APIView):
    authentication_classes = [EmployeeJWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Add a new permission",
        request_body=PermissionSerializer,
        responses={
            201: openapi.Response(
                "Permission added successfully", PermissionSerializer
            ),
            400: "Bad Request",
        },
        examples={
            "application/json": {
                "permission_group": "permission_group_id",
                "name": "permission name",
            }
        },
    )
    def post(self, request):
        serializer = PermissionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Permission added successfully", "data": serializer.data},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EditPermissionGroupView(APIView):
    authentication_classes = [EmployeeJWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Update a permission group",
        request_body=PermissionGroupSerializer,
        responses={
            200: openapi.Response(
                "Permission group updated successfully", PermissionGroupSerializer
            ),
            400: "Bad Request",
            404: "Not Found",
        },
        examples={
            "application/json": {
                "name": "Updated Group Name",
            }
        },
    )
    def put(self, request, group_id):
        group = get_object_or_404(PermissionGroup, id=group_id)
        serializer = PermissionGroupSerializer(group, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "message": "Permission group updated successfully.",
                    "data": serializer.data,
                }
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Partial update of a permission group",
        request_body=PermissionGroupSerializer,
        responses={
            200: openapi.Response(
                "Permission group updated successfully", PermissionGroupSerializer
            ),
            400: "Bad Request",
            404: "Not Found",
        },
        examples={
            "application/json": {
                "name": "Updated Group Name",
            }
        },
    )
    def patch(self, request, group_id):
        group = get_object_or_404(PermissionGroup, id=group_id)
        serializer = PermissionGroupSerializer(group, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "message": "Permission group updated successfully.",
                    "data": serializer.data,
                }
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EditPermissionsInGroup(APIView):
    authentication_classes = [EmployeeJWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Bulk update of permissions in a group",
        request_body=PermissionSerializer(many=True),
        responses={
            200: openapi.Response(
                "Permissions updated successfully", PermissionSerializer(many=True)
            ),
            400: "Bad Request",
            404: "Not Found",
            500: "Internal Server Error",
        },
        examples={
            "application/json": [
                {"id": 1, "name": "Updated Permission Name"},
                {"id": 2, "name": "Updated Permission Name"},
            ]
        },
    )
    def put(self, request, group_id):
        permission_group = get_object_or_404(PermissionGroup, id=group_id)
        permissions_data = request.data  # Access data directly

        try:
            # Normalize data to always be a list
            if isinstance(permissions_data, dict):
                permissions_data = [permissions_data]
            elif not isinstance(permissions_data, list):
                return Response(
                    {
                        "error": "Invalid data format. Expected a list of permissions or a single permission."
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Validate each item in the list to ensure it's a dictionary with an 'id' key
            permission_ids = []
            for perm in permissions_data:
                if isinstance(perm, dict) and "id" in perm:
                    permission_ids.append(perm["id"])
                else:
                    return Response(
                        {
                            "error": f"Invalid permission data: {perm}. Each permission must be a dictionary with an 'id' key."
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )

            # Update permission details and collect updated permissions
            updated_permissions = []
            for perm in permissions_data:
                permission_instance = get_object_or_404(Permission, id=perm["id"])
                serializer = PermissionSerializer(
                    permission_instance, data=perm, partial=True
                )
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                    updated_permissions.append(permission_instance)

            # Set the updated permissions in the permission group
            permission_group.permissions.set(updated_permissions)

            # Serialize the updated permissions
            serializer = PermissionSerializer(updated_permissions, many=True)

            return Response(
                {
                    "message": "Permissions updated successfully.",
                    "data": serializer.data,
                },
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class PermissionGroupDetailView(APIView):
    authentication_classes = [EmployeeJWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Get details of a specific permission group",
        responses={200: PermissionGroupSerializer(), 404: "Not Found"},
    )
    def get(self, request, group_id):
        permission_group = get_object_or_404(PermissionGroup, id=group_id)
        serializer = PermissionGroupSerializer(permission_group)
        return Response(serializer.data)


class AddPermissionsToGroupView(APIView):
    authentication_classes = [EmployeeJWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Add permissions to a permission group",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "permissions": openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Items(
                        type=openapi.TYPE_OBJECT,
                        properties={"name": openapi.Schema(type=openapi.TYPE_STRING)},
                    ),
                )
            },
            required=["permissions"],
        ),
        responses={
            201: "Permissions added to group successfully.",
            400: "Bad Request",
            404: "Permission group not found",
        },
        examples={
            "application/json": {
                "permissions": [{"name": "permission1"}, {"name": "permission2"}]
            }
        },
    )
    def post(self, request, group_id):
        try:
            group = PermissionGroup.objects.get(id=group_id)
        except PermissionGroup.DoesNotExist:
            return Response(
                {"message": "Permission group not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        permissions = request.data.get("permissions", [])
        print(permissions)
        if not permissions:
            return Response(
                {"message": "No permissions provided"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        errors = []
        for perm_data in permissions:
            perm_data["permission_group"] = group.id
            serializer = PermissionSerializer(data=perm_data)
            if serializer.is_valid():
                serializer.save()
            else:
                errors.append(serializer.errors)

        if errors:
            return Response({"errors": errors}, status=status.HTTP_400_BAD_REQUEST)

        return Response(
            {"message": "Permissions added to group successfully."},
            status=status.HTTP_201_CREATED,
        )


class DeletePermissionsFromGroupView(APIView):
    authentication_classes = [EmployeeJWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Delete permissions from a permission group",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "permissions": openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Items(type=openapi.TYPE_INTEGER),
                )
            },
            required=["permissions"],
        ),
        responses={
            204: "Permissions deleted from group successfully.",
            400: "Bad Request",
            404: "Permission group not found",
        },
        examples={"application/json": {"permissions": [1, 2, 3]}},
    )
    def delete(self, request, group_id):
        try:
            group = PermissionGroup.objects.get(id=group_id)
        except PermissionGroup.DoesNotExist:
            return Response(
                {"message": "Permission group not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        permissions = request.data.get("permissions", [])
        if not isinstance(permissions, list) or not all(
            isinstance(p, int) for p in permissions
        ):
            return Response(
                {"message": "Invalid data format"}, status=status.HTTP_400_BAD_REQUEST
            )

        # Ensure that the permissions exist and belong to the given group
        existing_permissions = Permission.objects.filter(
            id__in=permissions, permission_group=group
        )
        if not existing_permissions.exists():
            return Response(
                {"message": "No matching permissions found in the group"},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Delete the permissions
        deleted_count, _ = existing_permissions.delete()
        if deleted_count == 0:
            return Response(
                {"message": "No permissions were deleted"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            {"message": "Permissions deleted from group successfully."},
            status=status.HTTP_204_NO_CONTENT,
        )


class DeletePermissionGroupView(APIView):
    authentication_classes = [EmployeeJWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Delete a permission group",
        responses={
            204: "Permission group deleted successfully.",
            404: "Permission group not found",
        },
    )
    def delete(self, request, group_id):
        try:
            group = PermissionGroup.objects.get(id=group_id)
        except PermissionGroup.DoesNotExist:
            return Response(
                {"message": "Permission group not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        group.delete()
        return Response(
            {"message": "Permission group deleted successfully."},
            status=status.HTTP_204_NO_CONTENT,
        )


class RolesListView(APIView):
    authentication_classes = [EmployeeJWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Retrieve a list of all roles",
        responses={200: RoleSerializer(many=True)},
    )
    def get(self, request, *args, **kwargs):
        # Retrieve all roles
        roles = Role.objects.all()

        paginator = PageNumberPagination()
        paginator.page_size = settings.REST_FRAMEWORK["PAGE_SIZE"]

        # Paginate the queryset
        paginated_roles = paginator.paginate_queryset(roles, request)

        # Serialize paginated data
        serializer = RoleSerializer(paginated_roles, many=True)

        # Return paginated response
        return paginator.get_paginated_response(serializer.data)


class AddRoleView(APIView):
    authentication_classes = [EmployeeJWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Add a new role",
        request_body=RoleSerializer,
        responses={
            201: openapi.Response("Role added successfully.", RoleSerializer),
            400: "Bad Request",
        },
        examples={"application/json": {"name": "Admin", "permissions": [1, 2, 3]}},
    )
    def post(self, request):
        serializer = RoleSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save(created_by=request.user)
            return Response(
                {"message": "Success", "data": serializer.data},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EditRoleView(APIView):
    authentication_classes = [EmployeeJWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Edit a role by ID",
        request_body=RoleSerializer,
        responses={
            200: openapi.Response("Role updated successfully.", RoleSerializer),
            400: "Bad Request",
            404: "Role not found",
        },
    )
    def put(self, request, role_id):
        try:
            role = Role.objects.get(id=role_id)
        except Role.DoesNotExist:
            return Response(
                {"message": "Role not found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = RoleSerializer(role, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Role updated successfully.", "data": serializer.data}
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Partially update a role by ID",
        request_body=RoleSerializer,
        responses={
            200: openapi.Response("Role updated successfully.", RoleSerializer),
            400: "Bad Request",
            404: "Role not found",
        },
    )
    def patch(self, request, role_id):
        try:
            role = Role.objects.get(id=role_id)
        except Role.DoesNotExist:
            return Response(
                {"message": "Role not found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = RoleSerializer(role, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Role updated successfully.", "data": serializer.data}
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteRoleView(APIView):
    authentication_classes = [EmployeeJWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Delete a role by ID",
        responses={204: "Role deleted successfully.", 404: "Role not found"},
    )
    def delete(self, request, role_id):
        try:
            role = Role.objects.get(id=role_id)
        except Role.DoesNotExist:
            return Response(
                {"message": "Role not found"}, status=status.HTTP_404_NOT_FOUND
            )

        role.delete()
        return Response(
            {"message": "Role deleted successfully."}, status=status.HTTP_204_NO_CONTENT
        )


class RoleDetailView(APIView):
    authentication_classes = [EmployeeJWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Retrieve details of a role by ID",
        responses={200: RoleSerializer, 404: "Role not found"},
    )
    def get(self, request, role_id):
        try:
            role = Role.objects.get(id=role_id)
        except Role.DoesNotExist:
            return Response(
                {"message": "Role not found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = RoleSerializer(role)
        return Response(serializer.data)


class SyncPermissionsToRoleView(APIView):
    authentication_classes = [EmployeeJWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Sync permissions to a role by ID",
        request_body=SyncPermissionsSerializer,
        responses={
            200: "Permissions synced successfully.",
            400: "Bad Request",
            404: "Role not found",
        },
        examples={"application/json": {"permissions": [1, 2, 3]}},
    )
    def post(self, request, role_id):
        role = get_object_or_404(Role, id=role_id)
        serializer = SyncPermissionsSerializer(data=request.data)

        if serializer.is_valid():
            permission_ids = serializer.validated_data["permissions"]
            permissions = Permission.objects.filter(id__in=permission_ids)

            if len(permissions) != len(permission_ids):
                return Response(
                    {"message": "One or more permissions are invalid."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Clear existing permissions
            Role_has_Permission.objects.filter(role=role).delete()

            # Add new permissions
            for permission in permissions:
                Role_has_Permission.objects.create(role=role, permission=permission)

            return Response(
                {"message": "Permissions synced successfully."},
                status=status.HTTP_200_OK,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AddPermissionsToRoleView(APIView):
    authentication_classes = [EmployeeJWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Add permissions to a role by ID",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "permissions": openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Items(type=openapi.TYPE_STRING),
                )
            },
            required=["permissions"],
        ),
        responses={
            201: "Permissions added to role successfully.",
            400: "Bad Request",
            404: "Role not found",
        },
        examples={"application/json": {"permissions": ["permission1", "permission2"]}},
    )
    def post(self, request, role_id):
        try:
            role = Role.objects.get(id=role_id)
        except Role.DoesNotExist:
            return Response(
                {"message": "Role not found"}, status=status.HTTP_404_NOT_FOUND
            )

        permissions = request.data.get("permissions", [])
        if not permissions:
            return Response(
                {"message": "No permissions provided"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        errors = []
        for perm_name in permissions:
            try:
                permission = Permission.objects.get(name=perm_name)
                role.role_permissions.create(permission=permission)
            except Permission.DoesNotExist:
                errors.append(
                    {"permission_name": perm_name, "error": "Permission not found"}
                )

        if errors:
            return Response({"errors": errors}, status=status.HTTP_400_BAD_REQUEST)

        return Response(
            {"message": "Permissions added to role successfully."},
            status=status.HTTP_201_CREATED,
        )
