from asyncio.log import logger
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg import openapi
from .models import ScreeningInterviewTemplate, JobProfileInterview
from job_seekers.models import JobProfileAssessment, JobProfile
from drf_yasg.utils import swagger_auto_schema
from .serializers import (
    ScreeningInterviewTemplateSerializer,
    JobProfileInterviewSerializer,
)
from worktually_v3_api.custom_jwt.jwt import JobSeekerJWTAuthentication



class ScreeningInterviewTemplateQuestionsView(generics.RetrieveAPIView):
    authentication_classes = [JobSeekerJWTAuthentication]
    serializer_class = ScreeningInterviewTemplateSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        # Return an empty queryset for schema generation context
        if getattr(self, "swagger_fake_view", False):
            return ScreeningInterviewTemplate.objects.none()
        return ScreeningInterviewTemplate.objects.all()


class RetrieveInterviewQuestionsView(APIView):
    """
    API View to retrieve interview questions based on the provided job profile ID.
    """
    
    @swagger_auto_schema(
        operation_description="Retrieve interview questions based on the provided job profile ID.",
        manual_parameters=[
            openapi.Parameter(
                'job_profile_id',
                openapi.IN_QUERY,
                description="ID of the job profile for which to retrieve interview questions",
                type=openapi.TYPE_INTEGER,
                required=True
            )
        ],
        responses={
            200: openapi.Response(
                description="Interview questions retrieved successfully",
                examples={
                    "application/json": {
                        "status": "success",
                        "data": [
                            {
                                "id": 1,
                                "name": "Technical Interview",
                                "status": "active",
                                "questions": "What is polymorphism?",
                            },
                        ],
                    }
                },
            ),
            400: openapi.Response(
                description="Bad Request - Job profile ID is missing.",
                examples={
                    "application/json": {
                        "status": "error",
                        "message": "Job profile ID is required.",
                    }
                },
            ),
            403: openapi.Response(
                description="Forbidden - User is not authorized to view the interview questions.",
                examples={
                    "application/json": {
                        "status": "error",
                        "message": "User is not authorized to view interview questions.",
                    }
                },
            ),
            404: openapi.Response(
                description="Not Found - Job profile or assessment not found.",
                examples={
                    "application/json": {
                        "status": "error",
                        "message": "Job profile or assessment not found.",
                    }
                },
            ),
            500: openapi.Response(
                description="Internal server error.",
                examples={
                    "application/json": {
                        "status": "error",
                        "message": "An error occurred while retrieving interview questions.",
                    }
                },
            ),
        }
    )
    def get(self, request):
        job_profile_id = request.query_params.get("job_profile_id")
        
        if not job_profile_id:
            return self._build_error_response("Job profile ID is required.", status.HTTP_400_BAD_REQUEST)

        job_profile = self._get_job_profile(job_profile_id)
        if isinstance(job_profile, Response):
            return job_profile
        
        assessment = self._get_job_profile_assessment(job_profile)
        if isinstance(assessment, Response):
            return assessment

        return self._get_interview_templates()

    def _get_job_profile(self, job_profile_id):
        """Retrieve the job profile by ID."""
        try:
            return JobProfile.objects.get(id=job_profile_id)
        except JobProfile.DoesNotExist:
            logger.error(f"Job profile not found for ID: {job_profile_id}")
            return self._build_error_response("Job profile not found.", status.HTTP_404_NOT_FOUND)

    def _get_job_profile_assessment(self, job_profile):
        """Retrieve the job profile assessment and check the status."""
        try:
            assessment = JobProfileAssessment.objects.get(job_profile=job_profile)
            if assessment.status.lower() != "pass":
                logger.debug(f"Assessment status: {assessment.status}")
                return self._build_error_response(
                    "User is not authorized to view interview questions.", 
                    status.HTTP_403_FORBIDDEN
                )
            return assessment
        except JobProfileAssessment.DoesNotExist:
            logger.error(f"Job profile assessment not found for profile ID: {job_profile.id}")
            return self._build_error_response("Job profile assessment not found.", status.HTTP_404_NOT_FOUND)

    def _get_interview_templates(self):
        """Fetch and serialize interview templates."""
        interview_templates = ScreeningInterviewTemplate.objects.filter(status="Active")
        
        if not interview_templates.exists():
            logger.error("No active interview templates found.")
            return self._build_error_response("No interview templates found.", status.HTTP_404_NOT_FOUND)

        serializer = ScreeningInterviewTemplateSerializer(interview_templates, many=True)
        logger.debug(f"Interview Templates: {serializer.data}")
        
        return Response(
            {"status": "success", "data": serializer.data},
            status=status.HTTP_200_OK,
        )

    @staticmethod
    def _build_error_response(message, status_code):
        """Helper method to build error responses."""
        return Response({"status": "error", "message": message}, status=status_code)


class JobProfileInterviewSubmitView(generics.CreateAPIView):
    authentication_classes = [JobSeekerJWTAuthentication]
    queryset = JobProfileInterview.objects.all()
    serializer_class = JobProfileInterviewSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        serializer.save()

    def create(self, request, *args, **kwargs):
        data = request.data
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(
            {"message": "Answers submitted successfully"},
            status=status.HTTP_201_CREATED,
        )
