# apps.py
from django.apps import AppConfig
import sys
import threading

class EmployeeConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "employee"

    def ready(self):
        from employee import signals

        if 'runserver' in sys.argv or 'gunicorn' in sys.argv:
            def start_scheduler_safely():
                import time
                time.sleep(2)  # wait for DB to be ready
                try:
                    from employee.scheduler import start_employee_scheduler
                    start_employee_scheduler()
                except Exception as e:
                    print("[Scheduler Error] Failed to start scheduler:", str(e))

            threading.Thread(target=start_scheduler_safely).start()
