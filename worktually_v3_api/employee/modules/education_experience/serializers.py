from rest_framework import serializers
from .models import Education, Experience
from employee.models import Employee


class EducationSerializer(serializers.ModelSerializer):
    employee_id = serializers.PrimaryKeyRelatedField(
        queryset=Employee.objects.all(), source="employee"
    )

    class Meta:
        model = Education
        ref_name = "EmployeeEducationSerializer"
        fields = [
            "employee_id",
            "degree_title",
            "degree_type",
            "score",
            "major_subjects",
            "date_of_completion",
            "institute_name",
            "degree_certificate",
        ]

    def validate_employee_id(self, value):
        if value is None:
            raise serializers.ValidationError("Employee ID is required")
        return value

    def create(self, validated_data):
        # Extract employee_id from validated_data
        employee_id = validated_data.pop("employee_id")

        # Create the education instance with the validated data
        education = Education.objects.create(employee_id=employee_id, **validated_data)
        return education


class ExperienceSerializer(serializers.ModelSerializer):
    employee_id = serializers.PrimaryKeyRelatedField(
        queryset=Employee.objects.all(), source="employee"
    )

    class Meta:
        model = Experience
        fields = [
            "employee_id",
            "job_title",
            "company_name",
            "job_type",
            "start_date",
            "end_date",
            "description",
            "experience_letter",
        ]

    def validate_employee_id(self, value):
        if value is None:
            raise serializers.ValidationError("Employee ID is required")
        return value

    def create(self, validated_data):
        # Extract employee_id from validated_data
        employee_id = validated_data.pop("employee_id")

        # Create the experience instance with the validated data
        experience = Experience.objects.create(
            employee_id=employee_id, **validated_data
        )
        return experience
