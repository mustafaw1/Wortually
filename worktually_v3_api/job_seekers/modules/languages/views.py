from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from worktually_v3_api.custom_jwt.jwt import JobSeekerJWTAuthentication
from .models import Language
from .serializers import LanguageSerializer

class AddLanguageView(APIView):
    authentication_classes = [JobSeekerJWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=LanguageSerializer,
        responses={
            201: openapi.Response("Language added successfully.", LanguageSerializer),
            400: "Bad Request",
        },
        operation_description="Add a language entry.",
        examples={
            "application/json": {
                "language": "English",
                "proficiency": "Advanced",
            }
        },
    )
    def post(self, request):
        # The job_seeker will be automatically set in the serializer
        serializer = LanguageSerializer(data=request.data, context={'request': request})
        
        if serializer.is_valid():
            language = serializer.save()
            return Response(
                {
                    "status": "success",
                    "message": "Language added successfully",
                    "data": LanguageSerializer(language).data  # Return the added language data
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UpdateLanguageView(APIView):
    authentication_classes = [JobSeekerJWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=LanguageSerializer,
        responses={
            200: openapi.Response("Language updated successfully.", LanguageSerializer),
            400: "Bad Request",
            404: "Not Found",
        },
        operation_description="Update a language entry.",
        examples={
            "application/json": {
                "language": "English",
                "proficiency": "Advanced",
            }
        },
    )
    def put(self, request, language_id):
        # Retrieve the specific language entry for the logged-in user
        try:
            language = Language.objects.get(id=language_id, job_seeker=request.user)
        except Language.DoesNotExist:
            return Response(
                {"status": "error", "message": "Language entry not found for the logged-in user."},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Update the language entry with the new data
        serializer = LanguageSerializer(language, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            updated_language = serializer.save()
            return Response(
                {
                    "status": "success",
                    "message": "Language updated successfully",
                    "data": LanguageSerializer(updated_language).data  # Return the updated language data
                },
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DeleteLanguageView(APIView):
    authentication_classes = [JobSeekerJWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        responses={200: "Language deleted successfully.", 404: "Not Found"},
        operation_description="Delete a language entry.",
    )
    def delete(self, request, language_id):
        # Retrieve the specific language entry for the logged-in user
        try:
            language = Language.objects.get(id=language_id, job_seeker=request.user)
        except Language.DoesNotExist:
            return Response(
                {"status": "error", "message": "Language entry not found for the logged-in user."},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Serialize the language entry data before deletion
        language_data = LanguageSerializer(language).data
        
        # Delete the language entry
        language.delete()
        return Response(
            {
                "status": "success",
                "message": "Language deleted successfully.",
                "data": language_data  # Return the deleted language data
            },
            status=status.HTTP_200_OK,
        )