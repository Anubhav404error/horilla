from django.apps import AppConfig, apps
import sys


class LeaveConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "leave"

    def ready(self):
        from django.urls import include, path
        from horilla.horilla_settings import APPS
        from horilla.urls import urlpatterns
        from leave import signals

        APPS.append("leave")
        urlpatterns.append(
            path("leave/", include("leave.urls")),
        )

        if not any(cmd in sys.argv for cmd in ['makemigrations', 'migrate', 'collectstatic', 'shell', 'loaddata', 'createsuperuser']):
            try:
                from leave.scheduler import start  # ✅ Correct import
                start()  # ✅ Correct call to start scheduler
            except Exception as e:
                print("Error starting leave scheduler:", str(e))

        super().ready()
