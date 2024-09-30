from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from employee.models import Employee, OTP
from .serializers import (
    RegisterSerializer,
    LoginSerializer,
    EmployeesSerializer,
    LogoutSerializer,
    VerifyOTPSerializer,
    ResetPasswordRequestSerializer,
    ForgetPasswordSerializer,
    RoleSerializer,
    EmployeeTokenObtainPairSerializer,
)
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.conf import settings
from job_seekers.models import JobSeeker
from job_seekers.modules.accounts.serializers import JobSeekerTokenObtainPairSerializer
from django.shortcuts import get_object_or_404


class RegisterView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        request_body=RegisterSerializer,
        responses={
            201: openapi.Response("User registered successfully.", EmployeesSerializer),
            400: "Bad Request",
        },
        operation_description="Register a new user.",
        examples={
            "application/json": {
                "first_name": "John",
                "last_name": "Doe",
                "email": "john.doe@example.com",
                "password": "strong_password",
                "confirm_password": "strong_password",
                "phone": "1234567890",
            }
        },
    )
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                EmployeesSerializer(user).data, status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        request_body=LoginSerializer,
        responses={
            200: openapi.Response(
                description="Login successful",
                examples={
                    "application/json": {
                        "message": "Login successful",
                        "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
                        "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
                    }
                },
            ),
            401: "Invalid email or password",
            400: "Bad Request",
        },
    )
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            password = serializer.validated_data["password"]
            user = authenticate(request, email=email, password=password)

            if user is not None:
                if isinstance(user, Employee):
                    token_serializer = EmployeeTokenObtainPairSerializer
                elif isinstance(user, JobSeeker):
                    token_serializer = JobSeekerTokenObtainPairSerializer
                else:
                    return Response(
                        {"message": "Invalid user type"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                refresh = token_serializer.get_token(user)

                return Response(
                    {
                        "status": "success",
                        "refresh": str(refresh),
                        "access": str(refresh.access_token),
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"message": "Invalid email or password"},
                    status=status.HTTP_401_UNAUTHORIZED,
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=LogoutSerializer,
        responses={200: "Logout successful", 400: "Bad Request"},
    )
    def post(self, request):
        serializer = LogoutSerializer(data=request.data)
        if serializer.is_valid():
            logout(request)
            return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ForgetPasswordView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        request_body=ForgetPasswordSerializer,
        responses={200: "OTP has been sent to your email.", 400: "Bad Request"},
    )
    def post(self, request):
        serializer = ForgetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            otp_code = OTP.generate_otp()
            OTP.objects.create(email=email, otp=otp_code)
            send_mail(
                "Your OTP Code",
                f"Your OTP code is {otp_code}",
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )
            return Response(
                {"message": "OTP has been sent to your email."},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyOTPView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        request_body=VerifyOTPSerializer,
        responses={
            200: "Success",
            400: "Bad Request",
        },
    )
    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        if serializer.is_valid():
            otp_instance = OTP.objects.get(
                email=serializer.validated_data["email"],
                otp=serializer.validated_data["otp"],
            )
            otp_instance.is_verified = True
            otp_instance.save()
            return Response(
                {
                    "message": "Success.",
                    "email": otp_instance.email,
                    "token": otp_instance.reset_token,
                },
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        request_body=ResetPasswordRequestSerializer,
        responses={200: "Password reset successfully.", 400: "Bad Request"},
    )
    def post(self, request):
        serializer = ResetPasswordRequestSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            token = serializer.validated_data["token"]
            new_password = serializer.validated_data["new_password"]

            otp_instance = OTP.objects.filter(
                email=email, reset_token=token, is_verified=True
            ).first()
            if otp_instance:
                user = get_object_or_404(Employee, email=email)
                user.set_password(new_password)
                user.save()
                otp_instance.delete()
                return Response(
                    {"message": "Success"},
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"message": "Invalid or expired token."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        return Response({"message": "Provide your new password and token."})
