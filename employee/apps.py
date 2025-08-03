from django.apps import AppConfig
import sys

class EmployeeConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "employee"

    def ready(self):
        # Load signals safely
        try:
            import employee.signals
        except Exception as e:
            print("[Signal Error] Failed to load signals:", str(e))

        # Start scheduler only in server context
        if any(cmd in sys.argv for cmd in ["runserver", "gunicorn", "uwsgi"]):
            try:
                from employee.scheduler import start_employee_scheduler
                start_employee_scheduler()
            except Exception as e:
                print("[Scheduler Error] Failed to start scheduler:", str(e))
