from django.urls import path
from .views import *

urlpatterns = [
    path(
        "job-offers/<int:job_offer_id>/action/",
        AcceptRejectJobOfferView.as_view(),
        name="job_offer_action",
    ),
]
