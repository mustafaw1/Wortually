from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from .models import Organization
from .serializers import OrganizationSerializer
from worktually_v3_api.custom_jwt.jwt import EmployeeJWTAuthentication


class OrganizationListCreateView(APIView):
    authentication_classes = [EmployeeJWTAuthentication]

    def get(self, request):
        organizations = Organization.objects.all()
        serializer = OrganizationSerializer(organizations, many=True)
        return Response(
            {"message": "Success", "data": serializer.data}, status=status.HTTP_200_OK
        )

    def post(self, request):
        serializer = OrganizationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "message": "Organization created successfully",
                    "data": serializer.data,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {"message": "Validation error", "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )


class OrganizationDetailView(APIView):
    authentication_classes = [EmployeeJWTAuthentication]

    def get(self, request, pk):
        try:
            organization = Organization.objects.get(pk=pk)
            serializer = OrganizationSerializer(organization)
            return Response(
                {"message": "Success", "data": serializer.data},
                status=status.HTTP_200_OK,
            )
        except Organization.DoesNotExist:
            return Response({"message": "Not Found"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        try:
            organization = Organization.objects.get(pk=pk)
        except Organization.DoesNotExist:
            return Response({"message": "Not Found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = OrganizationSerializer(
            organization, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "message": "Organization updated successfully",
                    "data": serializer.data,
                },
                status=status.HTTP_200_OK,
            )
        return Response(
            {"message": "Validation error", "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )

    def delete(self, request, pk):
        try:
            organization = Organization.objects.get(pk=pk)
            organization.delete()
            return Response(
                {"message": "Organization deleted successfully"},
                status=status.HTTP_204_NO_CONTENT,
            )
        except Organization.DoesNotExist:
            return Response({"message": "Not Found"}, status=status.HTTP_404_NOT_FOUND)
