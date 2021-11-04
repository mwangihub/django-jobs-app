from django.apps import AppConfig


class JobsConfig(AppConfig):
    name = 'jobs'

    def ready(self) -> None:
        import jobs.signals