from django.urls import path
from . import views

urlpatterns = [
    path(
        "interview/questions/<int:pk>/",
        views.ScreeningInterviewTemplateQuestionsView.as_view(),
        name="interview-questions",
    ),
    path(
        "retrieve_interview_questions/",
        views.RetrieveInterviewQuestionsView.as_view(),
        name="retrieve_interview_questions",
    ),
    path(
        "interview/submit/",
        views.JobProfileInterviewSubmitView.as_view(),
        name="interview-submit",
    ),
]
