from django.urls import path
from .views import SendJobOfferView, RetrieveJobOfferView

urlpatterns = [
    path("send-job-offer/", SendJobOfferView.as_view(), name="send-job-offer"),
    path(
        "job-offers/<int:job_offer_id>/",
        RetrieveJobOfferView.as_view(),
        name="retrieve_job_offer",
    ),
]
