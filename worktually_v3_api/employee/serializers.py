from rest_framework import serializers
from .models import Employee, Experience, Dependent
from .modules.education_experience.serializers import EducationSerializer
from rest_framework import serializers
from .models import Employee, Role
from django.contrib.auth import get_user_model

User = get_user_model()


class UserProfileSerializer(serializers.ModelSerializer):
    role = serializers.CharField(
        source="role.name", required=False
    )  # This allows inputting role as a string

    class Meta:
        model = Employee
        fields = "__all__"

    def validate_role(self, role_name):
        try:
            role = Role.objects.get(name=role_name)
        except Role.DoesNotExist:
            raise serializers.ValidationError(
                f"Role with name '{role_name}' does not exist."
            )
        return role

    def create(self, validated_data):
        role_name = validated_data.pop("role", None)
        user_profile = Employee.objects.create(**validated_data)
        if role_name:
            user_profile.role = self.validate_role(role_name["name"])
            user_profile.save()
        return user_profile

    def update(self, instance, validated_data):
        role_name = validated_data.pop("role", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if role_name:
            instance.role = self.validate_role(role_name["name"])
        instance.save()
        return instance


class BankAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ["bank_name", "iban", "account_name", "bank_currency"]

    def validate(self, data):
        if not all(
            data.get(field)
            for field in ["bank_name", "iban", "account_name", "bank_currency"]
        ):
            raise serializers.ValidationError(
                "All fields in bank account information are required."
            )
        return data


class ExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experience
        fields = "__all__"


class DependentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dependent
        fields = "__all__"
