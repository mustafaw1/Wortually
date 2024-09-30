# from rest_framework import status
# from rest_framework.response import Response
# from rest_framework.views import APIView
# from rest_framework.permissions import IsAuthenticated
# from drf_yasg.utils import swagger_auto_schema
# from drf_yasg import openapi

# from .serializers import SkillSerializer

# class SkillsListView(APIView):
#     permission_classes = [IsAuthenticated]

#     @swagger_auto_schema(
#         responses={200: openapi.Response('List of skills', SkillSerializer(many=True))},
#         operation_description="Get list of skills"
#     )
#     def get(self, request):
#         skills = Skill.objects.filter(user=request.user)
#         serializer = SkillSerializer(skills, many=True)
#         return Response(serializer.data)

# class AddSkillView(APIView):
#     permission_classes = [IsAuthenticated]

#     @swagger_auto_schema(
#         request_body=SkillSerializer,
#         responses={
#             201: openapi.Response('Skill added successfully.', SkillSerializer),
#             400: 'Bad Request'
#         },
#         operation_description="Add a new skill",
#         examples={
#             'application/json': {
#                 'skill': 'Python Programming',
#                 'skill_level': 'Expert'
#             }
#         }
#     )
#     def post(self, request):
#         serializer = SkillSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save(user=request.user)
#             return Response({"message": "Skill added successfully.", "data": serializer.data}, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class DeleteSkillView(APIView):
#     permission_classes = [IsAuthenticated]

#     @swagger_auto_schema(
#         responses={204: 'Skill deleted successfully.', 404: 'Skill not found'},
#         operation_description="Delete a skill by ID"
#     )
#     def delete(self, request, skill_id):
#         try:
#             skill = Skill.objects.get(id=skill_id, user=request.user)
#         except Skill.DoesNotExist:
#             return Response({"message": "Skill not found"}, status=status.HTTP_404_NOT_FOUND)

#         skill.delete()
#         return Response({"message": "Your skill has been deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
