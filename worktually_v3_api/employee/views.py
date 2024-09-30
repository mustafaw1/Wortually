from django.shortcuts import render

from rest_framework import generics
from .models import Employee, Education, Experience, Dependent
from .serializers import (
    UserProfileSerializer,
    EducationSerializer,
    ExperienceSerializer,
    DependentSerializer,
    BankAccountSerializer,
)
from .modules.education_experience.views import (
    EditEducationView,
    AddEducationView,
    DeleteEducationView,
    EducationsListView,
)


class EmployeesList(generics.ListAPIView):
    queryset = Employee.objects.all()
    serializer_class = UserProfileSerializer


class AddEmployee(generics.CreateAPIView):
    serializer_class = UserProfileSerializer


class EmployeeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Employee.objects.all()
    serializer_class = UserProfileSerializer


class EditBasicInformation(generics.UpdateAPIView):
    queryset = Employee.objects.all()
    serializer_class = UserProfileSerializer


class EditWorkInformation(generics.UpdateAPIView):
    queryset = Employee.objects.all()
    serializer_class = UserProfileSerializer


class EditPersonalInformation(generics.UpdateAPIView):
    queryset = Employee.objects.all()
    serializer_class = UserProfileSerializer


class EditBankAccount(generics.UpdateAPIView):
    queryset = Employee.objects.all()
    serializer_class = BankAccountSerializer


class EditEmergencyInformation(generics.UpdateAPIView):
    queryset = Employee.objects.all()
    serializer_class = UserProfileSerializer


class ExperiencesList(generics.ListCreateAPIView):
    queryset = Experience.objects.all()
    serializer_class = ExperienceSerializer


class EditExperience(generics.RetrieveUpdateDestroyAPIView):
    queryset = Experience.objects.all()
    serializer_class = ExperienceSerializer


class EducationsList(generics.ListCreateAPIView):
    queryset = Education.objects.all()
    serializer_class = EducationSerializer


class EditEducation(generics.RetrieveUpdateDestroyAPIView):
    queryset = Education.objects.all()
    serializer_class = EducationSerializer


class DependentsList(generics.ListCreateAPIView):
    queryset = Dependent.objects.all()
    serializer_class = DependentSerializer


class EditDependent(generics.RetrieveUpdateDestroyAPIView):
    queryset = Dependent.objects.all()
    serializer_class = DependentSerializer


class ChangeProfilePicture(generics.UpdateAPIView):
    queryset = Employee.objects.all()
    serializer_class = UserProfileSerializer


class ChangeCoverPicture(generics.UpdateAPIView):
    queryset = Employee.objects.all()
    serializer_class = UserProfileSerializer
