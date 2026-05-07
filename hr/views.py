from django.shortcuts import render
from django.utils.timezone import now
from django.db.models import Count

from .models import Employee, Attendance, LeaveRequest, Department


def hr_dashboard(request):
    today = now().date()

    # ✅ Only EMPLOYEE role users (MATCH CASE 🔥)
    employees = Employee.objects.select_related('user', 'department')

    total_employees = employees.count()

    # ✅ Attendance counts
    present_count = Attendance.objects.filter(date=today, status="PRESENT").count()
    late_count = Attendance.objects.filter(date=today, status="LATE").count()

    # ✅ Marked employees today
    marked_today = Attendance.objects.filter(date=today).values_list('employee_id', flat=True)

    # ✅ ABSENT FIX (only from employees list 🔥)
    absent_count = employees.exclude(id__in=marked_today).count()

    # ✅ Leave count
    leave_count = LeaveRequest.objects.filter(status="APPROVED").count()

    departments = Department.objects.annotate(
    total=Count('employee')
)
    # ✅ Latest leave requests
    leave_requests = LeaveRequest.objects.select_related(
        'employee__user'
    ).order_by('-created_at')[:5]

    context = {
        "present_count": present_count,
        "absent_count": absent_count,
        "late_count": late_count,
        "leave_count": leave_count,
        "employees": employees,
        "departments": departments,
        "leave_requests": leave_requests,
    }
    print("total:",total_employees)

    return render(request, "hrmanagement.html", context)