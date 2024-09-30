from django.urls import path
from .views import *

urlpatterns = [
    path(
        "get-assessment-questions/",
        GetAssessmentQuestionsView.as_view(),
        name="get_assessment_questions",
    ),
    path(
        "submit_assessment_results/",
        AssessmentResultView.as_view(),
        name="assessment_results",
    ),
    path("get_results/", GetResultsView.as_view(), name="get_results"),
]
