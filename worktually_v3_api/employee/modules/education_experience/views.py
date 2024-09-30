from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Education
from .serializers import EducationSerializer
from .models import Experience
from .serializers import ExperienceSerializer
from rest_framework.pagination import PageNumberPagination
from django.conf import settings
from worktually_v3_api.custom_jwt.jwt import EmployeeJWTAuthentication


class EducationsListView(APIView):
    authentication_classes = [EmployeeJWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Get a list of all educations for the authenticated user",
        responses={200: EducationSerializer(many=True)},
    )
    def get(self, request, *args, **kwargs):
        # Retrieve all educations
        educations = Education.objects.all()

        paginator = PageNumberPagination()
        paginator.page_size = settings.REST_FRAMEWORK["PAGE_SIZE"]
        # Paginate the queryset
        paginated_educations = paginator.paginate_queryset(educations, request)

        # Serialize paginated data
        serializer = EducationSerializer(paginated_educations, many=True)

        # Return paginated response
        return paginator.get_paginated_response(serializer.data)


class AddEducationView(APIView):
    authentication_classes = [EmployeeJWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Add a new education record for the authenticated user",
        request_body=EducationSerializer,
        responses={
            201: openapi.Response("Education added successfully", EducationSerializer)
        },
        examples={
            "application/json": {
                "employee": 35,
                "degree_title": "Bachelor of Science",
                "degree_type": "B.Sc.",
                "score": "3.5 GPA",
                "major_subjects": "Computer Science",
                "date_of_completion": "2022-05-30",
                "institute_name": "University of Example",
                "degree_certificate": None,
            }
        },
    )
    def post(self, request, *args, **kwargs):
        serializer = EducationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(employee_id=request.data.get("employee_id"))
            return Response(
                {"message": "Education added successfully", "data": serializer.data},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EditEducationView(APIView):
    authentication_classes = [EmployeeJWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Update an existing education record for the authenticated user",
        request_body=EducationSerializer,
        responses={
            200: openapi.Response(
                "Education updated successfully", EducationSerializer
            ),
            404: "Education not found",
            400: "Bad request",
        },
        examples={
            "application/json": {
                "degree_title": "Master of Science",
                "degree_type": "M.Sc.",
                "score": "4.0 GPA",
                "major_subjects": "Data Science",
                "date_of_completion": "2024-05-30",
                "institute_name": "Example Institute",
                "degree_certificate": None,
            }
        },
    )
    def put(self, request, pk, *args, **kwargs):
        try:
            education = Education.objects.get(pk=pk)
        except Education.DoesNotExist:
            return Response(
                {"message": "Education not found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = EducationSerializer(education, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Education updated successfully", "data": serializer.data}
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Partially update an existing education record for the authenticated user",
        request_body=EducationSerializer,
        responses={
            200: openapi.Response(
                "Education updated successfully", EducationSerializer
            ),
            404: "Education not found",
            400: "Bad request",
        },
        examples={"application/json": {"score": "3.8 GPA"}},
    )
    def patch(self, request, education_id, *args, **kwargs):
        try:
            education = Education.objects.get(id=education_id, user=request.user)
        except Education.DoesNotExist:
            return Response(
                {"message": "Education not found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = EducationSerializer(education, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Education updated successfully."})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteEducationView(APIView):
    authentication_classes = [EmployeeJWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Delete an existing education record for the authenticated user",
        responses={
            204: "Your education has been deleted successfully.",
            404: "Education not found",
        },
    )
    def delete(self, request, pk, *args, **kwargs):
        try:
            education = Education.objects.get(pk=pk)
        except Education.DoesNotExist:
            return Response(
                {"message": "Education not found"}, status=status.HTTP_404_NOT_FOUND
            )

        education.delete()
        return Response(
            {"message": "Education deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )


class ExperiencesListView(APIView):
    authentication_classes = [EmployeeJWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Get a list of all experiences for the authenticated user",
        responses={200: ExperienceSerializer(many=True)},
    )
    def get(self, request, *args, **kwargs):
        # Retrieve all educations
        Experience = Experience.objects.all()

        paginator = PageNumberPagination()
        paginator.page_size = settings.REST_FRAMEWORK["PAGE_SIZE"]
        # Paginate the queryset
        paginated_educations = paginator.paginate_queryset(Experience, request)

        # Serialize paginated data
        serializer = ExperienceSerializer(paginated_educations, many=True)

        # Return paginated response
        return paginator.get_paginated_response(serializer.data)


class AddExperienceView(APIView):
    authentication_classes = [EmployeeJWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Add a new experience record for the authenticated user",
        request_body=ExperienceSerializer,
        responses={
            201: openapi.Response("Experience added successfully", ExperienceSerializer)
        },
        examples={
            "application/json": {
                "employee_id": int,
                "job_title": "HR Head",
                "company_name": "Invo Technologies",
                "job_type": "Part-time",
                "start_date": "2022-01-05",
                "end_date": "2023-01-01",
                "description": "Worked on cooking",
            }
        },
    )
    def post(self, request, *args, **kwargs):
        serializer = ExperienceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(employee_id=request.data.get("employee_id"))
            return Response(
                {"message": "Experience added successfully", "data": serializer.data},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EditExperienceView(APIView):
    authentication_classes = [EmployeeJWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Update an existing experience record for the authenticated user",
        request_body=ExperienceSerializer,
        responses={
            200: openapi.Response(
                "Experience updated successfully", ExperienceSerializer
            ),
            404: "Experience not found",
            400: "Bad request",
        },
        examples={
            "application/json": {
                "job_title": "Senior Software Engineer",
                "company_name": "Tech Company",
                "job_type": "Full-time",
                "start_date": "2020-01-01",
                "end_date": "2023-01-01",
                "description": "Led various projects",
                "experience_letter": None,
            }
        },
    )
    def put(self, request, experience_id, *args, **kwargs):
        try:
            experience = Experience.objects.get(id=experience_id)
        except Experience.DoesNotExist:
            return Response(
                {"message": "Experience not found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = ExperienceSerializer(experience, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Experience updated successfully."})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Partially update an existing experience record for the authenticated user",
        request_body=ExperienceSerializer,
        responses={
            200: openapi.Response(
                "Experience updated successfully", ExperienceSerializer
            ),
            404: "Experience not found",
            400: "Bad request",
        },
        examples={"application/json": {"description": "Promoted to team lead"}},
    )
    def patch(self, request, experience_id, *args, **kwargs):
        try:
            experience = Experience.objects.get(id=experience_id, user=request.user)
        except Experience.DoesNotExist:
            return Response(
                {"message": "Experience not found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = ExperienceSerializer(experience, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Experience updated successfully."})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteExperienceView(APIView):
    authentication_classes = [EmployeeJWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Delete an existing experience record for the authenticated user",
        responses={
            204: "Your experience has been deleted successfully.",
            404: "Experience not found",
        },
    )
    def delete(self, request, experience_id, *args, **kwargs):
        try:
            experience = Experience.objects.get(id=experience_id)
        except Experience.DoesNotExist:
            return Response(
                {"message": "Experience not found"}, status=status.HTTP_404_NOT_FOUND
            )

        experience.delete()
        return Response(
            {"message": "Your experience has been deleted successfully."},
            status=status.HTTP_204_NO_CONTENT,
        )
