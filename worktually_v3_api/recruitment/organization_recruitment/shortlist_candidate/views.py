from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests
import os
from rest_framework.permissions import IsAuthenticated


class ShortlistCandidatesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        api_key = os.getenv("API_KEY")
        candidates_api_url = "https://seekerdev3-api.worktually.com/api/candidates/"
        headers = {"Authorization": f"Api-Key {api_key}"}

        try:
            response = requests.get(candidates_api_url, headers=headers)
            if response.status_code != 200:
                return Response(
                    {"error": "Unable to fetch candidates."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            candidates_data = response.json()
            candidates = candidates_data.get("data", [])

            if not candidates:
                return Response(
                    {"message": "No candidates found."},
                    status=status.HTTP_404_NOT_FOUND,
                )

            return Response(
                {"message": "Success", "data": candidates}, status=status.HTTP_200_OK
            )
        except requests.exceptions.RequestException as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
