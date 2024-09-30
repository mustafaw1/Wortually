from django.urls import path
from .views import StateListView

urlpatterns = [
    path("states/", StateListView.as_view(), name="state-list"),
]
