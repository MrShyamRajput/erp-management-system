from django.db import models


class CompanySettings(models.Model):
    """Singleton model — only 1 row ever (always use pk=1)."""
    name = models.CharField(max_length=200)
    logo = models.ImageField(upload_to="company/", blank=True, null=True)
    address = models.TextField(blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    currency = models.CharField(max_length=10, default="INR")
    timezone = models.CharField(max_length=50, default="Asia/Kolkata")
    financial_year_start = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name = "Company Settings"
        verbose_name_plural = "Company Settings"

    def __str__(self):
        return self.name or "Company Settings"


class LeavePolicy(models.Model):
    """2 rows — SICK and ANNUAL."""
    LEAVE_TYPES = (
        ("SICK", "Sick Leave"),
        ("ANNUAL", "Annual Leave"),
    )
    leave_type = models.CharField(max_length=20, choices=LEAVE_TYPES, unique=True)
    days_allowed = models.IntegerField(default=12)
    carry_forward = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Leave Policy"
        verbose_name_plural = "Leave Policies"

    def __str__(self):
        return self.get_leave_type_display()


class WorkingDays(models.Model):
    """7 rows — Mon to Sun."""
    DAYS = [
        ("MON", "Monday"),
        ("TUE", "Tuesday"),
        ("WED", "Wednesday"),
        ("THU", "Thursday"),
        ("FRI", "Friday"),
        ("SAT", "Saturday"),
        ("SUN", "Sunday"),
    ]
    day = models.CharField(max_length=3, choices=DAYS, unique=True)
    is_working = models.BooleanField(default=True)
    work_start = models.TimeField(default="09:00")
    work_end = models.TimeField(default="18:00")

    class Meta:
        verbose_name = "Working Day"
        verbose_name_plural = "Working Days"
        ordering = [
            models.Case(
                models.When(day="MON", then=0),
                models.When(day="TUE", then=1),
                models.When(day="WED", then=2),
                models.When(day="THU", then=3),
                models.When(day="FRI", then=4),
                models.When(day="SAT", then=5),
                models.When(day="SUN", then=6),
                default=7,
                output_field=models.IntegerField(),
            )
        ]

    def __str__(self):
        return self.get_day_display()