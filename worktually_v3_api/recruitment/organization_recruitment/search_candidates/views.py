from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from .serializers import CandidateSerializer
from recruitment.models import Candidate
from worktually_v3_api.custom_jwt.jwt import EmployeeJWTAuthentication


class CandidateSearchView(APIView):
    authentication_classes = [EmployeeJWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Search candidate by candidate ID",
        responses={
            200: openapi.Response(
                description="Success",
                examples={
                    "application/json": {
                        "success": True,
                        "message": "Candidate retrieved successfully",
                        "data": {
                            "id": 1,
                            "name": "Candidate 1",
                            "email": "candidate1@example.com",
                        },
                    }
                },
            ),
            404: openapi.Response(description="Candidate not found"),
            500: openapi.Response(description="API key not found or server error"),
        },
    )
    def get(self, request, pk):
        try:
            candidate = Candidate.objects.get(id=pk)
        except Candidate.DoesNotExist:
            return JsonResponse(
                {"success": False, "message": "Candidate not found"},
                status=404,
            )

        # Serialize the candidate data using the serializer
        serializer = CandidateSerializer(candidate)
        return JsonResponse(
            {
                "success": True,
                "message": "Candidate retrieved successfully",
                "data": serializer.data,
            },
            status=200,
        )
