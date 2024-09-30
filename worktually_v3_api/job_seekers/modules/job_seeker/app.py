from django.apps import AppConfig


class JobSeekerConfig(AppConfig):
    name = "job_seekers.modules.job_seeker"

    def ready(self):
        import job_seekers.modules.job_seeker.signals
