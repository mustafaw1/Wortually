from django.urls import path
from .views import ShortlistCandidatesView

urlpatterns = [
    path(
        "shortlist-candidates/",
        ShortlistCandidatesView.as_view(),
        name="shortlist-candidates",
    ),
]
