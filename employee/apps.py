from django.apps import AppConfig
import sys


class EmployeeConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "employee"

    def ready(self):
        from employee import signals

        # Only run the scheduler when NOT in a management command
        if 'runserver' in sys.argv or 'gunicorn' in sys.argv:
            try:
                from employee.scheduler import start_employee_scheduler
                start_employee_scheduler()
            except Exception as e:
                print("[Scheduler Error] Failed to start scheduler:", str(e))
