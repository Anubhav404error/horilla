from django.apps import AppConfig, apps
import sys  # needed to check command-line arguments


class LeaveConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "leave"

    def ready(self):
        from django.urls import include, path
        from horilla.horilla_settings import APPS
        from horilla.urls import urlpatterns
        from leave import signals

        # Register leave app's URL and signals
        APPS.append("leave")
        urlpatterns.append(
            path("leave/", include("leave.urls")),
        )

        # Only run the scheduler if not running a migration or other management command
        if not any(cmd in sys.argv for cmd in ['makemigrations', 'migrate', 'collectstatic', 'shell', 'loaddata', 'createsuperuser']):
            try:
                from leave.scheduler import leave_reset, scheduler
                if not scheduler.running:
                    scheduler.start()
            except Exception as e:
                # Log or print the exception for debugging (you can remove later)
                print("Error starting leave scheduler:", str(e))

        super().ready()
