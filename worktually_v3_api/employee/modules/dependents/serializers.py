from rest_framework import serializers
from .models import Dependent
from employee.models import Employee
from rest_framework import serializers
from .models import Dependent, Employee

from rest_framework import serializers
from .models import Dependent, Employee


class DependentSerializer(serializers.ModelSerializer):
    employee_id = serializers.PrimaryKeyRelatedField(queryset=Employee.objects.all())

    class Meta:
        model = Dependent
        fields = [
            "employee_id",
            "name",
            "relation",
            "id_number",
            "social_insurance_number",
        ]

    def create(self, validated_data):
        employee_id = validated_data.pop("employee_id")
        if not isinstance(employee_id, Employee):
            employee_id = Employee.objects.get(id=employee_id)
        dependent = Dependent.objects.create(employee_id=employee_id, **validated_data)
        return dependent

    def update(self, instance, validated_data):
        employee_id = validated_data.pop("employee_id")
        if not isinstance(employee_id, Employee):
            employee_id = Employee.objects.get(id=employee_id)
        instance.employee_id = employee_id
        instance.name = validated_data.get("name", instance.name)
        instance.relation = validated_data.get("relation", instance.relation)
        instance.id_number = validated_data.get("id_number", instance.id_number)
        instance.social_insurance_number = validated_data.get(
            "social_insurance_number", instance.social_insurance_number
        )
        instance.save()
        return instance
