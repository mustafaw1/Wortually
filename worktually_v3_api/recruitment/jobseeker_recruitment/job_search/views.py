from rest_framework import generics, status, serializers
from rest_framework.response import Response
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from .serializers import JobSearchSerializer
from recruitment.serializers import JobPostSerializer
from worktually_v3_api.custom_jwt.jwt import JobSeekerJWTAuthentication


class JobSearchView(generics.GenericAPIView):
    authentication_classes = [JobSeekerJWTAuthentication]
    serializer_class = JobSearchSerializer

    @swagger_auto_schema(
        operation_description="Search for job posts by job title ID",
        request_body=JobSearchSerializer,
        responses={
            200: openapi.Response(
                "Success",
                openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "message": openapi.Schema(type=openapi.TYPE_STRING),
                        "data": openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Items(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    "id": openapi.Schema(type=openapi.TYPE_INTEGER),
                                    "job_title_id": openapi.Schema(
                                        type=openapi.TYPE_INTEGER
                                    ),
                                    "description": openapi.Schema(
                                        type=openapi.TYPE_STRING
                                    ),
                                    "slug": openapi.Schema(type=openapi.TYPE_STRING),
                                    "salary_type_id": openapi.Schema(
                                        type=openapi.TYPE_INTEGER
                                    ),
                                    "amount": openapi.Schema(type=openapi.TYPE_INTEGER),
                                    "experience_required": openapi.Schema(
                                        type=openapi.TYPE_INTEGER
                                    ),
                                    "education_required": openapi.Schema(
                                        type=openapi.TYPE_STRING
                                    ),
                                    "skills": openapi.Schema(type=openapi.TYPE_STRING),
                                    "gender": openapi.Schema(type=openapi.TYPE_STRING),
                                    "status": openapi.Schema(type=openapi.TYPE_STRING),
                                    "closed_reason": openapi.Schema(
                                        type=openapi.TYPE_STRING
                                    ),
                                },
                            ),
                        ),
                    },
                ),
            ),
            400: "Bad Request",
        },
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            job_title_id = serializer.validated_data["job_title_id"]
            try:
                job_posts = serializer.search_jobs(job_title_id)
                job_post_serializer = JobPostSerializer(job_posts, many=True)
                return Response(
                    {
                        "message": "Success",
                        "data": job_post_serializer.data,
                    },
                    status=status.HTTP_200_OK,
                )
            except serializers.ValidationError as e:
                return Response(
                    {"message": "Fail", "errors": e.detail},
                    status=status.HTTP_404_NOT_FOUND,
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
