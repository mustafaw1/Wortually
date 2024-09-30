from job_seekers.models import JobProfile


def is_profile_eligible_for_assessment(job_seeker_id):
    job_profiles = JobProfile.objects.filter(
        job_seeker_id=job_seeker_id,
        completion_rate__gt=90,
    )

    return job_profiles.exists(), (
        job_profiles.first() if job_profiles.exists() else None
    )
