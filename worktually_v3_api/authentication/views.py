from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import login, authenticate, logout
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .serializers import (
    VerifyOTPSerializer,
)
from .models import OTP

# Employee = get_user_model()

# class RegisterView(APIView):
#     permission_classes = [AllowAny]

#     @swagger_auto_schema(
#         request_body=RegisterSerializer,
#         responses={
#             201: openapi.Response(
#                 description="User registered successfully",
#                 examples={
#                     'application/json': {
#                         'message': 'User registered successfully',
#                         'refresh': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...',
#                         'access': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...'
#                     }
#                 }
#             ),
#             400: "Bad Request"
#         }
#     )
#     def post(self, request):
#         serializer = RegisterSerializer(data=request.data)
#         if serializer.is_valid():
#             employee = serializer.save()
#             # Generate tokens for the newly registered employee
#             refresh = RefreshToken.for_user(employee)
#             return Response({
#                 'message': 'User registered successfully',
#                 'refresh': str(refresh),
#                 'access': str(refresh.access_token),
#             }, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class LoginView(APIView):
#     permission_classes = [AllowAny]

#     @swagger_auto_schema(
#         request_body=LoginSerializer,
#         responses={
#             200: openapi.Response(
#                 description="Login successful",
#                 examples={
#                     'application/json': {
#                         'message': 'Login successful',
#                         'refresh': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...',
#                         'access': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...'
#                     }
#                 }
#             ),
#             401: "Invalid email or password",
#             400: "Bad Request"
#         }
#     )
#     def post(self, request):
#         serializer = LoginSerializer(data=request.data)
#         if serializer.is_valid():
#             email = serializer.validated_data['email']
#             password = serializer.validated_data['password']
#             # Authenticate the user with email and password
#             user = authenticate(request, email=email, password=password)
#             if user is not None:
#                 # Log the user in
#                 login(request, user)
#                 # Generate tokens for the logged-in user
#                 refresh = RefreshToken.for_user(user)
#                 return Response({
#                     'message': 'Login successful',
#                     'refresh': str(refresh),
#                     'access': str(refresh.access_token),
#                 })
#             else:
#                 return Response({'message': 'Invalid email or password'}, status=status.HTTP_401_UNAUTHORIZED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class LogoutView(APIView):
#     permission_classes = [IsAuthenticated]

#     @swagger_auto_schema(
#         request_body=LogoutSerializer,
#         responses={
#             200: "Logout successful",
#             400: "Bad Request"
#         }
#     )
#     def post(self, request):
#         serializer = LogoutSerializer(data=request.data)
#         if serializer.is_valid():
#             logout(request)
#             return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class ForgetPasswordView(APIView):
#     permission_classes = [AllowAny]

#     @swagger_auto_schema(
#         request_body=ForgetPasswordSerializer,
#         responses={
#             200: "OTP has been sent to your email.",
#             400: "Bad Request"
#         }
#     )
#     def post(self, request):
#         serializer = ForgetPasswordSerializer(data=request.data)
#         if serializer.is_valid():
#             email = serializer.validated_data['email']
#             otp_code = OTP.generate_otp()
#             OTP.objects.create(email=email, otp=otp_code)
#             send_mail(
#                 'Your OTP Code',
#                 f'Your OTP code is {otp_code}',
#                 settings.EMAIL_HOST,
#                 [email],
#                 fail_silently=False,
#             )
#             return Response({"message": "OTP has been sent to your email."}, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyOTPView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        request_body=VerifyOTPSerializer,
        responses={
            200: "OTP verified successfully. A password reset link has been sent to your email.",
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
            reset_link = f"{request.scheme}://{request.get_host()}/api/reset-password/?token={otp_instance.reset_token}"
            send_mail(
                "Reset Your Password",
                f"Click the link to reset your password: {reset_link}",
                settings.DEFAULT_FROM_EMAIL,
                [otp_instance.email],
                fail_silently=False,
            )
            return Response(
                {
                    "message": "OTP verified successfully. A password reset link has been sent to your email."
                },
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class ResetPasswordView(APIView):
#     permission_classes = [AllowAny]

#     @swagger_auto_schema(
#         request_body=ResetPasswordRequestSerializer,
#         responses={
#             200: "Password reset successfully.",
#             400: "Bad Request"
#         }
#     )
#     def post(self, request):
#         serializer = ResetPasswordRequestSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({"message": "Password reset successfully."}, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
