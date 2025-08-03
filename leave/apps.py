from django.apps import AppConfig
import sys
import threading


class LeaveConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "leave"

    def ready(self):
        from leave import signals  # Your signal registration

        # Avoid starting scheduler during manage.py commands like migrate, etc.
        if any(cmd in sys.argv for cmd in [
            'makemigrations', 'migrate', 'collectstatic', 'shell',
            'loaddata', 'createsuperuser', 'test'
        ]):
            return

        def start_scheduler():
            try:
                from leave.scheduler import start
                start()
            except Exception as e:
                print("[Leave Scheduler Error]", str(e))

        # Run scheduler in a separate thread to avoid blocking app startup
        threading.Thread(target=start_scheduler).start()
