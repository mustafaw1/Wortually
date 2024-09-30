from rest_framework import serializers
from .models import PermissionGroup, Permission, Role, Role_has_Permission


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ["id", "permission_group", "name"]


class CustomPermissionListSerializer(serializers.ListSerializer):
    def update(self, instance, validated_data):
        # Map the validated data by permission ID for efficient lookup
        permission_mapping = {permission.id: permission for permission in instance}

        # Update existing permissions and create new ones if necessary
        updated_permissions = []
        for permission_data in validated_data:
            permission_id = permission_data.get("id")
            if permission_id is not None and permission_id in permission_mapping:
                # Update existing permission
                permission = permission_mapping[permission_id]
                permission.name = permission_data.get("name", permission.name)
                permission.save()
                updated_permissions.append(permission)
            else:
                # Create new permission
                updated_permissions.append(self.child.create(permission_data))

        # Return the list of updated permissions
        return updated_permissions


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ["id", "name", "permission_group"]
        list_serializer_class = CustomPermissionListSerializer


class PermissionGroupSerializer(serializers.ModelSerializer):
    permissions = PermissionSerializer(many=True, read_only=True)

    class Meta:
        model = PermissionGroup
        fields = ["id", "name", "permissions"]


class RoleSerializer(serializers.ModelSerializer):
    permissions = PermissionSerializer(many=True, read_only=True)

    class Meta:
        model = Role
        fields = ["id", "name", "permissions"]

    def create(self, validated_data):
        permissions_data = self.context["request"].data.get("permissions", [])
        role = Role.objects.create(
            name=validated_data["name"], created_by=self.context["request"].user
        )
        for permission_id in permissions_data:
            permission = Permission.objects.get(id=permission_id)
            Role_has_Permission.objects.create(role=role, permission=permission)
        return role

    def update(self, instance, validated_data):
        permissions_data = self.context["request"].data.get("permissions", [])
        Role_has_Permission.objects.filter(role=instance).delete()
        for permission_id in permissions_data:
            permission = Permission.objects.get(id=permission_id)
            Role_has_Permission.objects.create(role=instance, permission=permission)
        return instance

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        permissions = Permission.objects.filter(role_permissions__role=instance)
        representation["permissions"] = PermissionSerializer(
            permissions, many=True
        ).data
        return representation


class RolePermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role_has_Permission
        fields = ["id", "role", "permission"]


class SyncPermissionsSerializer(serializers.Serializer):
    permissions = serializers.ListField(
        child=serializers.IntegerField(), allow_empty=False
    )
