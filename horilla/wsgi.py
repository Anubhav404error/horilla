# horilla/wsgi.py

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "horilla.settings")
application = get_wsgi_application()

# Start schedulers (only in production, not during migration)
if os.environ.get("RUN_MAIN") == "true":  # prevents double execution
    try:
        from horilla.start_schedulers import start
        start()
    except Exception as e:
        print("Scheduler startup error:", e)
