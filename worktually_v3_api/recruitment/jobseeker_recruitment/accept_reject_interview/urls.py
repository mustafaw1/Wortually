from django.urls import path
from .views import AcceptRejectInterviewView, RescheduleInterviewView

urlpatterns = [
    path(
        "interview/accept-reject/<int:pk>/",
        AcceptRejectInterviewView.as_view(),
        name="accept-reject-interview",
    ),
    path(
        "interview/reschedule/<int:pk>/",
        RescheduleInterviewView.as_view(),
        name="reschedule-interview",
    ),
]
