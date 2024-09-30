from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import OTP
from rest_framework_simplejwt.tokens import RefreshToken

# class EmployeeSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['id', 'first_name', 'last_name', 'email', 'phone_number']

# class RegisterSerializer(serializers.ModelSerializer):
#     confirm_password = serializers.CharField(write_only=True)

#     class Meta:
#         model = User
#         fields = ['first_name', 'last_name', 'email', 'phone_number', 'password', 'confirm_password']
#         extra_kwargs = {'password': {'write_only': True}}

#     def validate(self, data):
#         if data['password'] != data['confirm_password']:
#             raise serializers.ValidationError("Passwords do not match")
#         return data

#     def create(self, validated_data):
#         validated_data.pop('confirm_password')
#         return User.objects.create_user(**validated_data)

# class LoginSerializer(serializers.Serializer):
#     email = serializers.EmailField()
#     password = serializers.CharField()

#     def validate(self, data):
#         email = data.get('email')
#         password = data.get('password')

#         if email and password:
#             user = authenticate(email=email, password=password)
#             if not user:
#                 raise serializers.ValidationError("Invalid email or password", code='authentication_failed')
#         else:
#             raise serializers.ValidationError("Both email and password are required", code='invalid_credentials')

#         data['user'] = user
#         return data

# class LogoutSerializer(serializers.Serializer):
#     pass


# class ForgetPasswordSerializer(serializers.Serializer):
#     email = serializers.EmailField()

#     def validate_email(self, value):
#         if not User.objects.filter(email=value).exists():
#             raise serializers.ValidationError("No user is associated with this email.")
#         return value


class VerifyOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)

    def validate(self, data):
        email = data.get("email")
        otp = data.get("otp")
        if not OTP.objects.filter(email=email, otp=otp, is_verified=False).exists():
            raise serializers.ValidationError("Invalid OTP.")
        return data


# class ResetPasswordRequestSerializer(serializers.Serializer):
#     email = serializers.EmailField()
#     token = serializers.UUIDField()
#     new_password = serializers.CharField(write_only=True)
#     confirm_password = serializers.CharField(write_only=True)

#     def validate(self, data):
#         email = data.get('email')
#         token = data.get('token')
#         if data['new_password'] != data['confirm_password']:
#             raise serializers.ValidationError("Passwords do not match.")
#         if not OTP.objects.filter(email=email, reset_token=token).exists():
#             raise serializers.ValidationError("Invalid or expired token.")
#         return data

#     def save(self):
#         validated_data = self.validated_data
#         otp_instance = OTP.objects.get(email=validated_data['email'], reset_token=validated_data['token'])
#         employee = User.objects.get(email=validated_data['email'])
#         employee.set_password(validated_data['new_password'])
#         employee.save()
#         # Invalidate the OTP and token after successful password reset
#         otp_instance.delete()
#         return validated_data
