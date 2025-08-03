import logging
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from django.db import connection
from django.db.utils import OperationalError

logger = logging.getLogger(__name__)

def leave_reset():
    try:
        if "leave_leavetype" not in connection.introspection.table_names():
            logger.warning("Table leave_leavetype not found. Skipping leave_reset.")
            return
    except OperationalError as e:
        logger.error(f"Database not ready: {e}")
        return

    from leave.models import LeaveType

    today = datetime.now().date()
    leave_types = LeaveType.objects.filter(reset=True)

    for leave_type in leave_types:
        available_leaves = leave_type.employee_available_leave.all()
        for available_leave in available_leaves:
            reset_date = available_leave.reset_date
            expired_date = available_leave.expired_date

            if reset_date == today:
                available_leave.update_carryforward()
                new_reset_date = available_leave.set_reset_date(
                    assigned_date=today, available_leave=available_leave
                )
                available_leave.reset_date = new_reset_date
                available_leave.save()

            if expired_date and expired_date <= today:
                new_expired_date = available_leave.set_expired_date(
                    available_leave=available_leave, assigned_date=today
                )
                available_leave.expired_date = new_expired_date
                available_leave.save()

        if leave_type.carryforward_expire_date and leave_type.carryforward_expire_date <= today:
            leave_type.carryforward_expire_date = leave_type.set_expired_date(today)
            leave_type.save()

def start():
    try:
        if "leave_leavetype" not in connection.introspection.table_names():
            logger.warning("leave_leavetype table not found. Skipping scheduler.")
            return
    except OperationalError as e:
        logger.error(f"Error checking DB readiness: {e}")
        return

    global scheduler
    scheduler = BackgroundScheduler()
    scheduler.add_job(leave_reset, "interval", seconds=20)
    scheduler.start()
    logger.info("Leave scheduler started.")
