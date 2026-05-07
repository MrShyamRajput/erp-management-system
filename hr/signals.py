from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.utils.timezone import now
from .models import Employee, Attendance
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save




@receiver(user_logged_in)
def mark_attendance_on_login(sender, request, user, **kwargs):
    try:
        employee = Employee.objects.get(user=user)
        today = now().date()

        # Check if already marked today
        attendance, created = Attendance.objects.get_or_create(
            employee=employee,
            date=today,
            defaults={'status': 'PRESENT'}
        )

        # If already exists → do nothing
    except Employee.DoesNotExist:
        pass

User = get_user_model()

@receiver(post_save, sender=User)
def create_employee(sender, instance, created, **kwargs):
    print("SIGNAL TRIGGERED", instance, created)
    if created and instance.role == "employee":
        Employee.objects.create(user=instance)