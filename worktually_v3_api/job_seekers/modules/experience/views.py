from django.http import Http404
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from job_seekers.modules.experience.models import JobProfileExperience
from job_seekers.modules.experience.serializers import JobProfileExperienceSerializer
from worktually_v3_api.custom_jwt.jwt import JobSeekerJWTAuthentication
from job_seekers.models import JobProfile


class AddExperienceView(generics.CreateAPIView):
    authentication_classes = [JobSeekerJWTAuthentication]
    queryset = JobProfileExperience.objects.all()
    serializer_class = JobProfileExperienceSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=JobProfileExperienceSerializer,
        responses={
            201: openapi.Response(
                "Experience added successfully.", JobProfileExperienceSerializer
            ),
            400: "Bad Request",
        },
        operation_description="Add a new job profile experience.",
    )
    def post(self, request, *args, **kwargs):
        # Extract job_profile_id from the request data
        job_profile_id = request.data.get('job_profile')
        if not job_profile_id:
            return Response(
                {"status": "error", "message": "Job profile ID is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Check if the job profile exists
        if not JobProfile.objects.filter(id=job_profile_id).exists():
            return Response(
                {"status": "error", "message": "Job profile not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Ensure the job profile is associated with the logged-in user (optional, depending on your business logic)
        # You might need to adjust this check based on your specific requirements.

        # Proceed with creating the experience
        serializer = self.get_serializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            experience = serializer.save()
            return Response(
                {
                    "status": "success",
                    "data": JobProfileExperienceSerializer(experience).data,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {"status": "error", "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )


class UpdateExperienceView(generics.UpdateAPIView):
    authentication_classes = [JobSeekerJWTAuthentication]
    queryset = JobProfileExperience.objects.all()
    serializer_class = JobProfileExperienceSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "pk"

    @swagger_auto_schema(
        request_body=JobProfileExperienceSerializer,
        responses={
            200: openapi.Response(
                "Experience updated successfully.", JobProfileExperienceSerializer
            ),
            400: "Bad Request",
            404: "Not Found",
        },
        operation_description="Update an existing job profile experience.",
    )

    def put(self, request, experience_id):
        try:
            # Fetch the specific experience entry for the logged-in user
            experience = JobProfileExperience.objects.get(id=experience_id)
        except JobProfileExperience.DoesNotExist:
            return Response(
                {"status": "error", "message": "Experience not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Update the experience entry with the new data
        serializer = JobProfileExperienceSerializer(experience, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            experience = serializer.save()
            return Response(
                {
                    "status": "success",
                    "message": "Experience updated successfully.",
                    "data": JobProfileExperienceSerializer(experience).data  
                },
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteExperienceView(generics.DestroyAPIView):
    authentication_classes = [JobSeekerJWTAuthentication]
    queryset = JobProfileExperience.objects.all()
    serializer_class = JobProfileExperienceSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "pk"

    @swagger_auto_schema(
        responses={
            204: "Experience deleted successfully.",
            400: "Bad Request",
            404: "Not Found",
        },
        operation_description="Delete a job profile experience.",
    )

    def delete(self, request, experience_id):


        try:
            # Fetch the specific experience entry for the logged-in user
            experience = JobProfileExperience.objects.get(id=experience_id)
        except JobProfileExperience.DoesNotExist:
            return Response(
                {"status": "error", "message": "Experience not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Serialize the experience data before deletion
        response_data = JobProfileExperienceSerializer(experience).data

        # Delete the experience entry
        experience.delete()
        return Response(
            {
                "status": "success",
                "message": "Experience deleted successfully.",
                "data": response_data  # Include deleted data in the response
            },
            status=status.HTTP_200_OK,
        )
