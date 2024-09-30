from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated
from lookups.models import City
from .serializers import CitySerializer
from drf_yasg import openapi


class CityView(APIView):
    @swagger_auto_schema(
        operation_description="Get cities by state ID",
        responses={
            200: CitySerializer(many=True),
            400: "State ID is required",
            404: "State not found",
        },
        manual_parameters=[
            openapi.Parameter(
                "state_id",
                openapi.IN_QUERY,
                description="state_id",
                type=openapi.TYPE_INTEGER,
                required=True,
            )
        ],
    )
    def get(self, request, *args, **kwargs):
        state_id = request.query_params.get("state_id", None)
        if not state_id:
            return Response(
                {"success": False, "message": "State ID is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        cities = City.objects.filter(state_id=state_id)
        if not cities.exists():
            return Response(
                {"success": False, "message": "No cities found for this state"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = CitySerializer(cities, many=True)
        return Response(
            {
                "message": "success",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )
