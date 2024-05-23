from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import Employee
from rest_framework_simplejwt.tokens import RefreshToken

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['id', 'first_name', 'last_name', 'email', 'phone_number']

class RegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = Employee
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'password', 'confirm_password']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match")
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        return Employee.objects.create_user(**validated_data)

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if email and password:
            user = authenticate(email=email, password=password)
            if not user:
                raise serializers.ValidationError("Invalid email or password", code='authentication_failed')
        else:
            raise serializers.ValidationError("Both email and password are required", code='invalid_credentials')

        data['user'] = user
        return data

class LogoutSerializer(serializers.Serializer):
    pass


# class PasswordResetSerializer(serializers.Serializer):
#     email = serializers.EmailField()

#     def validate_email(self, value):
#         try:
#             employee = Employee.objects.get(email=value)
#         except Employee.DoesNotExist:
#             raise serializers.ValidationError("No user is associated with this email address")
#         return value

# class PasswordResetConfirmSerializer(serializers.Serializer):
#     email = serializers.EmailField()
#     token = serializers.CharField()
#     password = serializers.CharField(write_only=True)
#     confirm_password = serializers.CharField(write_only=True)

#     def validate(self, data):
#         if data['password'] != data['confirm_password']:
#             raise serializers.ValidationError("Passwords do not match")
#         return data

#     def save(self):
#         email = self.validated_data['email']
#         token = self.validated_data['token']
#         password = self.validated_data['password']
        
#         try:
#             employee = Employee.objects.get(email=email)
#         except Employee.DoesNotExist:
#             raise serializers.ValidationError("Invalid email address")

#         refresh = RefreshToken(token)
#         if str(refresh.access_token) != token:
#             raise serializers.ValidationError("Invalid token")

#         employee.set_password(password)
#         employee.save()

class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        try:
            employee = Employee.objects.get(email=value)
        except Employee.DoesNotExist:
            raise serializers.ValidationError("No user is associated with this email address")
        return value

class PasswordResetConfirmSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match")
        return data

    def save(self):
        email = self.validated_data['email']
        password = self.validated_data['password']
        
        try:
            employee = Employee.objects.get(email=email)
        except Employee.DoesNotExist:
            raise serializers.ValidationError("Invalid email address")

        employee.set_password(password)
        employee.save()
