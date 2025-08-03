import datetime
from datetime import timedelta
from apscheduler.schedulers.background import BackgroundScheduler


def update_experience():
    from employee.models import EmployeeWorkInformation

    try:
        queryset = EmployeeWorkInformation.objects.filter(employee_id__is_active=True)
        for instance in queryset:
            instance.experience_calculator()
    except Exception as e:
        print("[Scheduler Error] update_experience failed:", e)


def block_unblock_disciplinary():
    from base.models import EmployeeShiftSchedule
    from employee.models import DisciplinaryAction
    from employee.policies import employee_account_block_unblock

    try:
        today = datetime.date.today()
        dis_action = DisciplinaryAction.objects.all()

        for dis in dis_action:
            if dis.action.block_option:
                if dis.action.action_type == "suspension":
                    employees = dis.employee_id.all()

                    if dis.days:
                        end_date = dis.start_date + timedelta(days=dis.days)
                        result = today >= end_date

                        for emp in employees:
                            employee_account_block_unblock(emp_id=emp.id, result=result)

                    elif dis.hours:
                        hour_str = dis.hours + ":00"
                        if hour_str > "00:00:00" and today >= dis.start_date:
                            for emp in employees:
                                shift = emp.employee_work_info.shift_id
                                shift_detail = EmployeeShiftSchedule.objects.filter(
                                    shift_id=shift
                                )
                                for shi in shift_detail:
                                    weekday_names = [
                                        "monday", "tuesday", "wednesday",
                                        "thursday", "friday", "saturday", "sunday"
                                    ]
                                    if weekday_names[today.weekday()] == shi.day.day:
                                        start_time = shi.start_time
                                        hour_time = datetime.datetime.strptime(
                                            hour_str, "%H:%M:%S"
                                        ).time()

                                        result_datetime = datetime.datetime.combine(
                                            today, start_time
                                        ) + timedelta(
                                            hours=hour_time.hour,
                                            minutes=hour_time.minute,
                                            seconds=hour_time.second,
                                        )
                                        current_time = datetime.datetime.now()
                                        result = current_time >= result_datetime

                                        employee_account_block_unblock(
                                            emp_id=emp.id, result=result
                                        )

                elif dis.action.action_type == "dismissal" and today >= dis.start_date:
                    for emp in dis.employee_id.all():
                        employee_account_block_unblock(emp_id=emp.id, result=False)

    except Exception as e:
        print("[Scheduler Error] block_unblock_disciplinary failed:", e)


def start_employee_scheduler():
    try:
        scheduler = BackgroundScheduler()
        scheduler.add_job(update_experience, "interval", hours=4)
        scheduler.add_job(block_unblock_disciplinary, "interval", seconds=25)
        scheduler.start()
        print("[Scheduler] Background jobs started successfully.")
    except Exception as e:
        print("[Scheduler Error] Failed to start scheduler:", str(e))
