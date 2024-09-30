from django.urls import path
from .views import (
    AddBasicProfileView,
    UpdateBasicProfileView,
    DeleteBasicProfileView,
    JobSeekerDetailView,
    ValidateTokenView,
    AddProfilePictureView,
    UpdateProfilePictureView,
    DeleteProfilePictureView
)

urlpatterns = [
    path("add/", AddBasicProfileView.as_view(), name="add_profile"),
    path(
        "update/<int:pk>/",
        UpdateBasicProfileView.as_view(),
        name="update_profile",
    ),
    path(
        "delete/<int:pk>/",
        DeleteBasicProfileView.as_view(),
        name="delete_profile",
    ),
    path("info/", JobSeekerDetailView.as_view(), name="job-seeker-detail"),
    path('validate-token/', ValidateTokenView.as_view(), name='validate-token'),
    path('profile-picture/add/', AddProfilePictureView.as_view(), name='add-profile-picture'),
    path('profile-picture/update/', UpdateProfilePictureView.as_view(), name='update-profile-picture'),
    path('profile-picture/delete/', DeleteProfilePictureView.as_view(), name='delete-profile-picture'),
]
