from django.urls import path
from .views import CandidateDetailView, CandidateListView

urlpatterns = [
    path("candidates/", CandidateListView.as_view(), name="candidate-list"),
    path(
        "candidates/<int:pk>/", CandidateDetailView.as_view(), name="candidate-detail"
    ),
]
