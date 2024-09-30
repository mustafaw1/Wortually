from django.urls import path
from .views import CandidateSearchView

urlpatterns = [
    path(
        "search-candidate/<int:pk>/",
        CandidateSearchView.as_view(),
        name="search-candidate",
    ),
]
