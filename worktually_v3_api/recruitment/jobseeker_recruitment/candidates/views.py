from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from .models import Candidate
from .serializers import CandidateSerializer
from rest_framework import permissions
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class CandidateListView(APIView):
    @swagger_auto_schema(
        operation_description="List all candidates",
        responses={
            200: openapi.Response("Success", CandidateSerializer(many=True)),
        },
    )
    def get(self, request):
        candidates = Candidate.objects.all()
        serializer = CandidateSerializer(candidates, many=True)
        return Response(
            {"message": "Success", "data": serializer.data}, status=status.HTTP_200_OK
        )


class CandidateDetailView(APIView):
    # permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_description="List all candidates that applied for a job",
        responses={
            200: openapi.Response("Success", CandidateSerializer(many=True)),
            404: "Not Found",
        },
    )
    def get(self, request, pk):
        try:
            candidate = Candidate.objects.get(pk=pk)
        except Candidate.DoesNotExist:
            return Response(
                {"message": "Candidate not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = CandidateSerializer(candidate)
        return Response(
            {"message": "Success", "data": serializer.data}, status=status.HTTP_200_OK
        )

    def patch(self, request, pk):
        try:
            candidate = Candidate.objects.get(pk=pk)
        except Candidate.DoesNotExist:
            return Response(
                {"message": "Candidate not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = CandidateSerializer(candidate, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "success", "data": serializer.data},
                status=status.HTTP_200_OK,
            )
        return Response(
            {"message": "Invalid data", "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )
