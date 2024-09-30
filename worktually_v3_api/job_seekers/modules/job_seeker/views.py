from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import JobSeeker
from .serializers import BasicProfileSerializer, ProfilePictureSerializer
from rest_framework import generics, status
from worktually_v3_api.custom_jwt.jwt import JobSeekerJWTAuthentication
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.exceptions import InvalidToken
from django.contrib.auth.models import User
from rest_framework.authentication import get_authorization_header
from django.contrib.auth import logout
from rest_framework_simplejwt.tokens import AccessToken


class JobSeekerDetailView(generics.RetrieveAPIView):
    authentication_classes = [JobSeekerJWTAuthentication]
    serializer_class = BasicProfileSerializer
    # permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        responses={
            200: openapi.Response("Success", BasicProfileSerializer),
            404: "Not Found",
        },
        operation_description="Retrieve the logged-in job seeker's profile.",
    )
    def get(self, request, *args, **kwargs):
        # `request.user` is the logged-in user
        profile = request.user
        serializer = self.get_serializer(profile)
        return Response(
            {"status": "success", "data": serializer.data},
            status=status.HTTP_200_OK,
        )


class AddBasicProfileView(APIView):
    authentication_classes = [JobSeekerJWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=BasicProfileSerializer,
        responses={
            201: openapi.Response(
                "Profile added successfully.", BasicProfileSerializer
            ),
            400: "Bad Request",
        },
        operation_description="Add a basic profile.",
        examples={
            "application/json": {
                "first_name": "John",
                "last_name": "Doe",
                "email": "john.doe@example.com",
                "phone": "1234567890",
                "birth_date": "1990-01-01",
                "gender": "Male",
                "country": "USA",
            }
        },
    )
    def post(self, request):
        serializer = BasicProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"status": "success", "message": "Job Seeker added successfully"},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateBasicProfileView(APIView):
    authentication_classes = [JobSeekerJWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=BasicProfileSerializer,
        responses={
            200: openapi.Response(
                "Profile updated successfully.", BasicProfileSerializer
            ),
            400: "Bad Request",
            404: "Not Found",
        },
        operation_description="Update a basic profile.",
        examples={
            "application/json": {
                "first_name": "John",
                "last_name": "Doe",
                "email": "john.doe@example.com",
                "phone": "1234567890",
                "birth_date": "1990-01-01",
                "gender": "Male",
                "country": "USA",
            }
        },
    )
    def put(self, request, pk):
        try:
            profile = JobSeeker.objects.get(pk=pk)
        except JobSeeker.DoesNotExist:
            return Response(
                {"status": "error", "message": "Profile not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = BasicProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"status": "success", "message": "Job Seeker updated successfully"},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteBasicProfileView(APIView):
    authentication_classes = [JobSeekerJWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        responses={200: "Profile deleted successfully.", 404: "Not Found"},
        operation_description="Delete a basic profile.",
    )
    def delete(self, request, pk):
        try:
            profile = JobSeeker.objects.get(pk=pk)
        except JobSeeker.DoesNotExist:
            return Response(
                {"status": "error", "message": "Profile not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        profile.delete()
        return Response(
            {"status": "success", "message": "Job Seeker deleted successfully"},
            status=status.HTTP_200_OK,
        )


class ValidateTokenView(APIView):
    def post(self, request):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return Response({"status": "error", "message": "Token not provided or incorrect format."}, status=status.HTTP_400_BAD_REQUEST)
        
        token = auth_header.split(' ')[1]
        
        try:
            # Decode the token using AccessToken to validate
            decoded_token = AccessToken(token)
            user_id = decoded_token.get("user_id")
            
            # Retrieve the user based on the decoded user_id
            user = JobSeeker.objects.filter(pk=user_id).first()
            
            if not user:
                raise InvalidToken("User not found.")
            
            # Prepare user data for response
            user_data = {
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
                "phone": user.phone,
                "birth_date":user.birth_date,
                "gender": user.gender,
            }
            
            return Response({"status": "success", "message": "Token is valid.", "user": user_data}, status=status.HTTP_200_OK)
        
        except InvalidToken:
            logout(request)  # Log out user if token is invalid
            return Response({"status": "error", "message": "Invalid token. User logged out."}, status=status.HTTP_401_UNAUTHORIZED)
        


class AddProfilePictureView(APIView):
    authentication_classes = [JobSeekerJWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=ProfilePictureSerializer,
        responses={
            201: openapi.Response(
                "Profile picture added successfully.", ProfilePictureSerializer
            ),
            400: "Bad Request",
        },
        operation_description="Add a profile picture for the logged-in job seeker.",
        examples={
            "multipart/form-data": {
                "profile_picture": "(File upload)",
                "profile_picture_url": "https://example.com/profile.jpg"
            }
        }
    )
    def post(self, request):
        user = request.user
        serializer = ProfilePictureSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "status": "success",
                    "message": "Profile picture added successfully.",
                    "data": serializer.data, 
                },
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    



class UpdateProfilePictureView(APIView):
    authentication_classes = [JobSeekerJWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=ProfilePictureSerializer,
        responses={
            200: openapi.Response(
                "Profile picture updated successfully.",
                ProfilePictureSerializer
            ),
            400: "Bad Request"
        },
        operation_description="Update the profile picture for the logged-in user.",
        examples={
            "application/json": {
                "profile_picture_url": "https://example.com/path/to/updated_profile_picture.jpg"
            }
        }
    )
    def put(self, request):
        user = request.user 
        serializer = ProfilePictureSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "status": "success", "message": "Profile picture updated successfully", 
                    "data": serializer.data,
                },
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteProfilePictureView(APIView):
    authentication_classes = [JobSeekerJWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        responses={
            204: "Profile picture deleted successfully.",
            400: "Bad Request"
        },
        operation_description="Delete the profile picture for the logged-in user and return the deleted profile picture URL."
    )
    def delete(self, request):
        user = request.user  # Get the logged-in user
        if user.profile_picture_url:
            deleted_url = user.profile_picture_url  # Store the URL before deletion
            user.profile_picture.delete(save=False)
            user.profile_picture_url = None
            user.save()

            return Response(
                {
                    "status": "success",
                    "message": "Profile picture deleted successfully",
                    "deleted_profile_picture_url": deleted_url,
                },
                status=status.HTTP_204_NO_CONTENT,
            )
        return Response(
            {"status": "error", "message": "No profile picture found."},
            status=status.HTTP_400_BAD_REQUEST
        )



