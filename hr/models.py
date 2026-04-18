from django.db import models

from django.conf import settings

class Department(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):  
        return self.name


class Employee(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    department = models.ForeignKey('Department', on_delete=models.SET_NULL, null=True)
    role = models.CharField(max_length=100)

    STATUS_CHOICES = (
        ("ACTIVE", "Active"),
        ("INACTIVE", "Inactive"),
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="ACTIVE")

    def __str__(self):
        return str(self.user)


class Attendance(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date = models.DateField()

    STATUS_CHOICES = (
        ("PRESENT", "Present"),
        ("ABSENT", "Absent"),
        ("LATE", "Late"),
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)

    def __str__(self):
        return f"{self.employee} - {self.date}"


class LeaveRequest(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)

    LEAVE_TYPES = (
        ("SICK", "Sick Leave"),
        ("ANNUAL", "Annual Leave"),
    )
    leave_type = models.CharField(max_length=20, choices=LEAVE_TYPES)

    reason = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()

    STATUS_CHOICES = (
        ("PENDING", "Pending"),
        ("APPROVED", "Approved"),
        ("REJECTED", "Rejected"),
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="PENDING")

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.employee} - {self.leave_type}"