from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .models import (
    Industry,
    Country,
    State,
    City,
    Designation,
    Department,
    Source,
    DegreeType,
    EmployeeType,
    JobType,
    Relation,
    Skills,
    Language,
    JobTitle
)
from .serializers import (
    IndustrySerializer,
    CountrySerializer,
    StateSerializer,
    CitySerializer,
    DesignationSerializer,
    DepartmentSerializer,
    SourceSerializer,
    DegreeTypeSerializer,
    EmployeeTypeSerializer,
    JobTypeSerializer,
    RelationSerializer,
    SkillsSerializer,
    LanguagesSerializer,
    JobTitleSerializer
)
from rest_framework.permissions import IsAuthenticated


class LookupBaseViewSet(viewsets.ModelViewSet):
    """
    Base viewset for lookup tables.
    """

    queryset = None  # To be overridden in subclasses
    serializer_class = None  # To be overridden in subclasses

    def get_queryset(self):
        if self.queryset is None:
            raise AssertionError("queryset is not set")
        return self.queryset

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(
            {
                "message": f"{self.serializer_class.Meta.model.__name__} added successfully",
                "data": serializer.data,
            },
            status=status.HTTP_201_CREATED,
        )

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(
            {
                "message": f"{self.serializer_class.Meta.model.__name__} updated successfully",
                "data": serializer.data,
            }
        )

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {
                "message": f"{self.serializer_class.Meta.model.__name__} deleted successfully"
            },
            status=status.HTTP_204_NO_CONTENT,
        )


class IndustryViewSet(LookupBaseViewSet):
    queryset = Industry.objects.all()
    serializer_class = IndustrySerializer
    pagination_class = None


class CountryViewSet(LookupBaseViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    pagination_class = None


class StateViewSet(LookupBaseViewSet):
    queryset = State.objects.all()
    serializer_class = StateSerializer
    pagination_class = None

class JobtitleViewSet(LookupBaseViewSet):
    queryset = JobTitle.objects.all()
    serializer_class = JobTitleSerializer
    pagination_class = None

class CityViewSet(LookupBaseViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    pagination_class = None


class DesignationViewSet(LookupBaseViewSet):
    queryset = Designation.objects.all()
    serializer_class = DesignationSerializer
    pagination_class = None


class DepartmentViewSet(LookupBaseViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    pagination_class = None


class SourceViewSet(LookupBaseViewSet):
    queryset = Source.objects.all()
    serializer_class = SourceSerializer
    pagination_class = None


class DegreeTypeViewSet(LookupBaseViewSet):
    queryset = DegreeType.objects.all()
    serializer_class = DegreeTypeSerializer
    pagination_class = None


class EmployeeTypeViewSet(LookupBaseViewSet):
    queryset = EmployeeType.objects.all()
    serializer_class = EmployeeTypeSerializer
    pagination_class = None


class JobTypeViewSet(LookupBaseViewSet):
    queryset = JobType.objects.all()
    serializer_class = JobTypeSerializer
    pagination_class = None


class RelationViewSet(LookupBaseViewSet):
    queryset = Relation.objects.all()
    serializer_class = RelationSerializer
    pagination_class = None


class SkillViewSet(LookupBaseViewSet):
    queryset = Skills.objects.all()
    serializer_class = SkillsSerializer
    pagination_class = None


class LanguageViewSet(LookupBaseViewSet):
    queryset = Language.objects.all()
    serializer_class = LanguagesSerializer
    pagination_class = None
