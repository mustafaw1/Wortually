from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    IndustryViewSet,
    DesignationViewSet,
    DepartmentViewSet,
    SourceViewSet,
    DegreeTypeViewSet,
    EmployeeTypeViewSet,
    JobTypeViewSet,
    RelationViewSet,
    SkillViewSet,
    LanguageViewSet,
    JobtitleViewSet
)

router = DefaultRouter()
router.register(r"industries", IndustryViewSet)
router.register(r"designations", DesignationViewSet)
router.register(r"departments", DepartmentViewSet)
router.register(r"sources", SourceViewSet)
router.register(r"degree-types", DegreeTypeViewSet)
router.register(r"employee-types", EmployeeTypeViewSet)
router.register(r"job-types", JobTypeViewSet)
router.register(r"relations", RelationViewSet)
router.register(r"skills", SkillViewSet)
router.register(r"languages", LanguageViewSet)
router.register(r"jobtitles", JobtitleViewSet)

urlpatterns = [
    path("api/", include(router.urls)),
    path("api/", include("lookups.modules.states.urls")),
    path("api/", include("lookups.modules.cities.urls")),
    path("api/", include("lookups.modules.countries.urls")),
    path("api/", include("lookups.modules.skills.urls")),
]
