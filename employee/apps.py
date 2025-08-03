from django.apps import AppConfig
import sys

class EmployeeConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "employee"

    def ready(self):
        # Safe import of signals
        try:
            import employee.signals
        except Exception as e:
            print("[Signal Error] Failed to load signals:", str(e))

        # Only start scheduler in runtime (not during migrations, shell, etc.)
        if any(cmd in sys.argv for cmd in ["runserver", "gunicorn", "uwsgi"]):
            try:
                from employee.scheduler import start_employee_scheduler
                start_employee_scheduler()
            except Exception as e:
                print("[Scheduler Error] Failed to start scheduler:", str(e))
