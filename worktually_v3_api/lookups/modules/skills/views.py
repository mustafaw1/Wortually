from rest_framework import generics
from lookups.models import SkillCategory
from .serializers import SkillSerializer, SkillCategorySerializer



class SkillCategoryListView(generics.ListAPIView):
    queryset = SkillCategory.objects.all()
    serializer_class = SkillCategorySerializer
    pagination_class = None
