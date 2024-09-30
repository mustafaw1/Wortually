from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from lookups.models import State, Country
from rest_framework.permissions import IsAuthenticated
from .serializers import StateSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class StateListView(APIView):
    @swagger_auto_schema(
        operation_description="Get all states for a specific country by country ID",
        responses={
            200: openapi.Response(
                description="Success",
                examples={
                    "application/json": {
                        "success": True,
                        "message": "States retrieved successfully",
                        "data": [
                            {"id": 1, "name": "State 1", "country": 1},
                            {"id": 2, "name": "State 2", "country": 1},
                        ],
                    }
                },
            ),
            400: openapi.Response(description="Bad Request"),
            404: openapi.Response(description="Country not found"),
        },
        manual_parameters=[
            openapi.Parameter(
                "country_id",
                openapi.IN_QUERY,
                description="Country ID",
                type=openapi.TYPE_INTEGER,
                required=True,
            )
        ],
    )
    def get(self, request):
        country_id = request.query_params.get("country_id")
        if not country_id:
            return Response(
                {"success": False, "message": "Country ID is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            country = Country.objects.get(id=country_id)
        except Country.DoesNotExist:
            return Response(
                {"success": False, "message": "Country not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        states = State.objects.filter(country=country)
        serializer = StateSerializer(states, many=True)
        return Response(
            {
                "message": "Success",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )
