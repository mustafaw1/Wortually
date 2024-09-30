# urls.py in the organization project
from django.urls import path
from .views import *

urlpatterns = [
    path(
        "send_interview-request/",
        SendInterviewRequestView.as_view(),
        name="list-candidates-send-interview-requests",
    ),
    path(
        "interviews/<int:pk>/accept-reject/",
        AcceptRejectInterviewView.as_view(),
        name="accept-reject-interview",
    ),
    path(
        "interviews/<int:pk>/reschedule/",
        RescheduleInterviewView.as_view(),
        name="reschedule-interview",
    ),
]
