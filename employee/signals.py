from django.db.models.signals import post_save
from django.dispatch import receiver
from employee.models import Employee


@receiver(post_save, sender=Employee)
def create_employee_profile(sender, instance, created, **kwargs):
    if created:
        # Add logic to create related data like EmployeeWorkInformation, etc.
        print(f"[Signal] Created new employee: {instance}")
