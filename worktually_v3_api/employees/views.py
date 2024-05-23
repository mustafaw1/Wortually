from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import login, authenticate
from .serializers import RegisterSerializer, LoginSerializer, LogoutSerializer, EmployeeSerializer
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import logout
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from .serializers import PasswordResetSerializer, PasswordResetConfirmSerializer
from django.conf import settings
Employee = get_user_model()

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            employee = serializer.save()
            # Generate tokens for the newly registered employee
            refresh = RefreshToken.for_user(employee)
            return Response({
                'message': 'Employee registered successfully',
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            # Authenticate the user with email and password
            user = authenticate(request, email=email, password=password)
            if user is not None:
                # Log the user in
                login(request, user)
                # Generate tokens for the logged-in user
                refresh = RefreshToken.for_user(user)
                return Response({
                    'message': 'Login successful',
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                })
            else:
                return Response({'message': 'Invalid email or password'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = LogoutSerializer(data=request.data)
        if serializer.is_valid():
            logout(request)
            return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class PasswordResetView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            employee = Employee.objects.get(email=email)
            refresh = RefreshToken.for_user(employee)
            reset_link = f"http://localhost:8000/password-reset-confirm?token={refresh.access_token}&email={email}"
            
            # For testing purposes, we'll just return the link in the response
            return Response({"reset_link": reset_link}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PasswordResetConfirmView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Password has been reset successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class PasswordResetView(APIView):
#     permission_classes = [AllowAny]

#     def post(self, request):
#         serializer = PasswordResetSerializer(data=request.data)
#         if serializer.is_valid():
#             email = serializer.validated_data['email']
#             employee = Employee.objects.get(email=email)
#             refresh = RefreshToken.for_user(employee)
#             reset_link = f"http://your-frontend-url/reset-password?token={refresh.access_token}&email={email}"
            
#             send_mail(
#                 subject="Password Reset Request",
#                 message=f"Use the following link to reset your password: {reset_link}",
#                 from_email=settings.DEFAULT_FROM_EMAIL,
#                 recipient_list=[email],
#                 fail_silently=False,
#             )
#             return Response({"message": "Password reset link has been sent to your email"}, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class PasswordResetConfirmView(APIView):
#     permission_classes = [AllowAny]

#     def post(self, request):
#         serializer = PasswordResetConfirmSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({"message": "Password has been reset successfully"}, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

