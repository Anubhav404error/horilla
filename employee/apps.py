from django.apps import AppConfig
import sys


class EmployeeConfig(AppConfig):
    """
    AppConfig for the 'employee' app.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "employee"

    def ready(self):
        # Import signals if any (optional)
        from employee import signals

        # Only start scheduler if not running management commands
        if not any(cmd in sys.argv for cmd in ['makemigrations', 'migrate', 'collectstatic', 'shell', 'loaddata', 'createsuperuser']):
            try:
                from employee.scheduler import run_disciplinary_scheduler, scheduler  # or whatever your function is called
                if not scheduler.running:
                    scheduler.start()
            except Exception as e:
                print("Error starting employee scheduler:", str(e))
