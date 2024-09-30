from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings


@shared_task
def send_interview_notification(
    email, first_name, job_post_id, interview_method_id, start_date, end_date
):
    """
    Celery task to send an interview notification email.
    """
    subject = "Interview Scheduled"
    message = (
        f"Dear {first_name},\n\n"
        f"You have an interview scheduled for {start_date}.\n\n"
        f"Details:\n"
        f"Job Post ID: {job_post_id}\n"
        f"Interview Method ID: {interview_method_id}\n"
        f"Start Date: {start_date}\n"
        f"End Date: {end_date}\n\n"
        f"Best regards,\n"
        f"Your Company"
    )

    send_mail(
        subject, message, settings.DEFAULT_FROM_EMAIL, [email], fail_silently=False
    )


@shared_task
def send_job_offer_notification(email, first_name, job_post_id, amount, currency):
    subject = "Job Offer Received"
    message = f"Hi {first_name},\n\nYou have received a job offer for the job post ID {job_post_id} with an offer of {amount} {currency}.\n\nBest regards,\nYour Company"
    send_mail(
        subject, message, settings.DEFAULT_FROM_EMAIL, [email], fail_silently=False
    )
