from django.db.models.signals import post_save, post_delete, pre_delete
from django.dispatch import receiver

from recruitment.models import Candidate, JobApplication

from job_seekers.models import (
    JobSeeker,
    Education,
    Language,
    JobProfileExperience,
    Skills,
    JobProfilePortfolio,
    JobProfileSkill,
)


@receiver(post_save, sender=JobSeeker)
def update_profile_completion_on_profile_picture_save(sender, instance, **kwargs):
    if 'profile_picture_url' in instance.__dict__:
        print("Profile picture URL updated, updating profile completion")
        instance.update_profile_completion()

@receiver(post_save, sender=Education)
def update_profile_completion_on_education_save(sender, instance, **kwargs):
    print("Education updated, updating profile completion")
    instance.job_seeker.update_profile_completion()


@receiver(post_save, sender=Language)
def update_profile_completion_on_language_save(sender, instance, **kwargs):
    print("Language updated, updating profile completion")
    instance.job_seeker.update_profile_completion()

@receiver(pre_delete, sender=JobProfileExperience)
@receiver(post_save, sender=JobProfileExperience)
@receiver(post_delete, sender=JobProfileExperience)
def update_profile_completion_on_experience_change(sender, instance, **kwargs):
    print("Experience updated, updating JobProfile completion")
    instance.job_profile.update_profile_completion()

@receiver(pre_delete, sender=JobProfilePortfolio)
@receiver(post_save, sender=JobProfilePortfolio)
@receiver(post_delete, sender=JobProfilePortfolio)
def update_profile_completion_on_portfolio_change(sender, instance, **kwargs):
    print("Portfolio updated, updating JobProfile completion")
    instance.job_profile.update_profile_completion()



@receiver(post_save, sender=JobProfileSkill)
@receiver(post_delete, sender=JobProfileSkill)
def update_profile_completion_on_skill_change(sender, instance, **kwargs):
    print("Skill updated, updating JobProfile completion")
    instance.job_profile.update_profile_completion()



# Signals for post_delete
@receiver(pre_delete, sender=JobSeeker)
def update_profile_completion_on_profile_picture_delete(sender, instance, **kwargs):
    if instance.profile_picture_url:
        instance.profile_picture_url = None
        print("Profile picture URL deleted, updating profile completion")
        instance.update_profile_completion()


@receiver(post_delete, sender=Education)
def update_profile_completion_on_education_delete(sender, instance, **kwargs):
    print("Education deleted, updating profile completion")
    instance.job_seeker.update_profile_completion()


@receiver(post_delete, sender=Language)
def update_profile_completion_on_language_delete(sender, instance, **kwargs):
    print("Language deleted, updating profile completion")
    instance.job_seeker.update_profile_completion()





@receiver(post_save, sender=JobApplication)
def create_candidate(sender, instance, created, **kwargs):
    if created:
        Candidate.objects.create(
            job_application_id=instance,
            job_profile_id=instance.job_profile,  # Assuming job_profile is a field in JobApplication
            job_seeker_id=instance.job_seeker,  # Assuming job_seeker is a field in JobApplication
            status="Applied",  # Set default status or update as needed
            expected_start_date=None,  # Set default value or leave it to be updated later
        )
