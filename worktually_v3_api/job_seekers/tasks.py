from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from recruitment.models import JobApplication, JobPost
from employee.models import Organization
from job_seekers.models import JobSeeker
from .email_templates import (
    get_job_application_email_subject,
    get_job_application_email_body,
)


@shared_task
def send_job_application_notification(job_application_id):
    # Get job application details
    try:
        job_application = JobApplication.objects.get(id=job_application_id)
    except JobApplication.DoesNotExist:
        raise Exception("Job application not found")

    job_post_id = job_application.job_id

    # Fetch job post details from the local database
    try:
        job_post = JobPost.objects.get(id=job_post_id)
    except JobPost.DoesNotExist:
        raise Exception("Job post not found")

    # Fetch organization details using the organization ID from the job post
    organization_id = job_post.organization_id
    try:
        organization = Organization.objects.get(id=organization_id)
    except Organization.DoesNotExist:
        raise Exception("Organization not found")

    organization_email = organization.email

    # Fetch job seeker details from the local database
    job_seeker_id = job_application.job_seeker.id
    try:
        job_seeker = JobSeeker.objects.get(id=job_seeker_id)
    except JobSeeker.DoesNotExist:
        raise Exception("Job seeker not found")

    # Send email notification
    subject = get_job_application_email_subject()
    body = get_job_application_email_body(
        organization, job_post, job_seeker, job_application
    )

    send_mail(
        subject,
        body,
        settings.DEFAULT_FROM_EMAIL,
        [organization_email],
        fail_silently=False,
    )
