from django.urls import path
from .views import SkillCategoryListView

urlpatterns = [
    path('skill-categories/', SkillCategoryListView.as_view(), name='skill-category-list'),
]