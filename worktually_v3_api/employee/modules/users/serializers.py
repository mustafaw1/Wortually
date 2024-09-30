from rest_framework import serializers
from .models import Employee, BankAccount, EmergencyContact
from employee.models import Role


class EmployeeSerializer(serializers.ModelSerializer):
    role = serializers.CharField()
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Employee
        fields = "__all__"

    def create(self, validated_data):
        role_name = validated_data.pop("role", None)
        password = validated_data.pop("password", None)

        if not role_name:
            raise serializers.ValidationError("Role is required.")

        role, created = Role.objects.get_or_create(name=role_name)
        employee = Employee.objects.create(role=role, **validated_data)

        # Create bank accounts
        BankAccount.objects.create(employee=employee)

        # Create emergency contacts
        EmergencyContact.objects.create(employee=employee)

        if password:
            employee.set_password(password)
            employee.save()
        return employee

    def update(self, instance, validated_data):
        role_name = validated_data.pop("role", None)
        password = validated_data.pop("password", None)
        if role_name:
            role, created = Role.objects.get_or_create(name=role_name)
            instance.role = role
        for key, value in validated_data.items():
            setattr(instance, key, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance


class EmployeeBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = [
            "first_name",
            "last_name",
            "email",
            "phone",
            "father_name",
            "location_id",
        ]


class EmployeeWorkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = [
            "reporting_to",
            "source_of_hiring",
            "date_of_joining",
            "employee_type",
            "exit_date",
            "status",
        ]


class EmployeePersonalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = [
            "first_name",
            "email",
            "date_of_birth",
            "id_number",
            "marital_status",
            "gender",
            "address",
        ]


class BankAccountSerializer(serializers.ModelSerializer):
    employee_id = serializers.IntegerField()

    class Meta:
        model = BankAccount
        fields = [
            "id",
            "employee_id",
            "bank_name",
            "iban",
            "account_number",
            "currency",
        ]

    def validate_employee_id(self, value):
        if not Employee.objects.filter(id=value).exists():
            raise serializers.ValidationError("Employee does not exist")
        return value


class EmergencyContactSerializer(serializers.ModelSerializer):
    employee_id = serializers.IntegerField()

    class Meta:
        model = EmergencyContact
        fields = [
            "id",
            "employee_id",
            "name",
            "email",
            "phone",
            "relation",
            "address",
            "country_id",
            "state_id",
            "city_id",
            "postal_code",
        ]

    def validate_employee_id(self, value):
        if not Employee.objects.filter(id=value).exists():
            raise serializers.ValidationError("Employee does not exist")
        return value


class ChangeProfilePictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ["picture"]


class ChangeCoverPictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ["cover_photo"]
