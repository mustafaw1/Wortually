from django.urls import path
from .views import CityView

urlpatterns = [
    path("cities/", CityView.as_view(), name="cities"),
]
