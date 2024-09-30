from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Dependent
from .serializers import DependentSerializer
from rest_framework.pagination import PageNumberPagination
from worktually_v3_api.custom_jwt.jwt import EmployeeJWTAuthentication


class DependentsListView(APIView):
    authentication_classes = [EmployeeJWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        responses={
            200: openapi.Response("List of dependents", DependentSerializer(many=True))
        },
        operation_description="Get list of dependents",
        examples={
            "application/json": [
                {
                    "id": 1,
                    "user": 1,
                    "name": "John Doe",
                    "relation": "Child",
                    "id_number": "12345",
                    "social_insurance_number": "67890",
                },
                {
                    "id": 2,
                    "user": 1,
                    "name": "Jane Doe",
                    "relation": "Spouse",
                    "id_number": "54321",
                    "social_insurance_number": "09876",
                },
            ]
        },
    )
    def get(self, request):
        dependents = Dependent.objects.order_by("id").all()

        # Initialize pagination class with page size from settings
        paginator = PageNumberPagination()
        paginator.page_size = settings.REST_FRAMEWORK["PAGE_SIZE"]

        # Paginate the queryset
        paginated_dependents = paginator.paginate_queryset(dependents, request)

        # Serialize paginated data
        serializer = DependentSerializer(paginated_dependents, many=True)

        # Return paginated response
        return paginator.get_paginated_response(serializer.data)


class AddDependentView(APIView):
    authentication_classes = [EmployeeJWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=DependentSerializer,
        responses={
            201: openapi.Response("Dependent added successfully.", DependentSerializer),
            400: "Bad Request",
        },
        operation_description="Add a new dependent",
        examples={
            "application/json": {
                "name": "John Doe",
                "relation": "Child",
                "id_number": "12345",
                "social_insurance_number": "67890",
            }
        },
    )
    def post(self, request):
        serializer = DependentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(employee_id=request.data.get("employee_id"))
            return Response(
                {"message": "Dependent added successfully", "data": serializer.data},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EditDependentView(APIView):
    authentication_classes = [EmployeeJWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=DependentSerializer,
        responses={
            200: openapi.Response(
                "Dependent updated successfully.", DependentSerializer
            ),
            400: "Bad Request",
            404: "Dependent not found.",
        },
        operation_description="Update an existing dependent by ID",
        examples={
            "application/json": {
                "name": "Updated John Doe",
                "relation": "Updated Child",
                "id_number": "54321",
                "social_insurance_number": "09876",
            }
        },
    )
    def put(self, request, dependent_id):
        try:
            dependent = Dependent.objects.get(id=dependent_id)
        except Dependent.DoesNotExist:
            return Response(
                {"error": "Dependent not found."}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = DependentSerializer(dependent, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Dependent updated successfully.", "data": serializer.data},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        request_body=DependentSerializer,
        responses={
            200: openapi.Response(
                "Dependent updated successfully.", DependentSerializer
            ),
            400: "Bad Request",
            404: "Dependent not found.",
        },
        operation_description="Partially update an existing dependent by ID",
        examples={"application/json": {"name": "Updated John Doe"}},
    )
    def patch(self, request, dependent_id):
        try:
            dependent = Dependent.objects.get(id=dependent_id, user=request.user)
        except Dependent.DoesNotExist:
            return Response(
                {"error": "Dependent not found."}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = DependentSerializer(dependent, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Dependent updated successfully.", "data": serializer.data},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteDependentView(APIView):
    authentication_classes = [EmployeeJWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        responses={200: openapi.Response("Dependent deleted successfully.")},
        operation_description="Delete an existing dependent by ID",
        examples={"application/json": {"message": "Dependent deleted successfully."}},
    )
    def delete(self, request, dependent_id):
        try:
            dependent = Dependent.objects.get(id=dependent_id)
        except Dependent.DoesNotExist:
            return Response(
                {"error": "Dependent not found."}, status=status.HTTP_404_NOT_FOUND
            )

        dependent.delete()
        return Response(
            {"message": "Dependent deleted successfully."}, status=status.HTTP_200_OK
        )
