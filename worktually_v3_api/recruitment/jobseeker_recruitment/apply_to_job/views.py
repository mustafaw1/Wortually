from rest_framework import generics, status
from rest_framework.response import Response
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from .serializers import JobApplicationSerializer
from recruitment.models import JobApplication
from job_seekers.models import JobProfile
from recruitment.models import JobPost
from worktually_v3_api.custom_jwt.jwt import JobSeekerJWTAuthentication
from rest_framework.permissions import IsAuthenticated


class ApplyToJobView(generics.CreateAPIView):
    authentication_classes = [JobSeekerJWTAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = JobApplicationSerializer

    @swagger_auto_schema(
        operation_description="Apply for a job",
        request_body=JobApplicationSerializer,
        responses={
            201: openapi.Response(
                "Job application submitted successfully.", JobApplicationSerializer
            ),
            400: "Bad Request",
        },
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            job_post_id = serializer.validated_data.get("job_id")
            job_profile_id = serializer.validated_data.get("job_profile").id

            # Check if JobPost exists
            if not JobPost.objects.filter(id=job_post_id).exists():
                return Response(
                    {"message": "Job post does not exist."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Check if JobProfile exists
            if not JobProfile.objects.filter(id=job_profile_id).exists():
                return Response(
                    {"message": "Job profile does not exist."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Save the job application and trigger the task
            serializer.save()
            return Response(
                {
                    "message": "Job application submitted successfully.",
                    "data": serializer.data,
                },
                status=status.HTTP_201_CREATED,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
