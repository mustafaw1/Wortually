from django.apps import AppConfig


class JobApplyConfig(AppConfig):
    name = "recruitment.jobseeker_recruitment.apply_to_job"

    def ready(self):
        import apply_to_job.signals  # Ensure the signals module is imported
