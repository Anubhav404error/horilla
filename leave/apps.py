from django.apps import AppConfig
import sys

class LeaveConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "leave"

    def ready(self):
        try:
            from django.urls import include, path
            from horilla.horilla_settings import APPS
            from horilla.urls import urlpatterns

            # Register app
            APPS.append("leave")
            urlpatterns.append(path("leave/", include("leave.urls")))

            # Load signals
            import leave.signals
        except Exception as e:
            print("[LeaveConfig] Error during setup:", e)

        # Avoid running scheduler during migration-related commands
        if not any(cmd in sys.argv for cmd in [
            'makemigrations', 'migrate', 'collectstatic', 'shell',
            'loaddata', 'createsuperuser', 'test'
        ]):
            try:
                from leave.scheduler import scheduler
                if not scheduler.running:
                    scheduler.start()
            except Exception as e:
                print("[LeaveConfig] Scheduler error:", str(e))
