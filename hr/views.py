from django.shortcuts import render
from django.utils.timezone import now
from django.db.models import Count
from .models import Employee, Attendance, LeaveRequest, Department


def hr_dashboard(request):
    today = now().date()

    # Attendance Stats
    present_count = Attendance.objects.filter(date=today, status="PRESENT").count()
    leave_count = LeaveRequest.objects.filter(status="APPROVED").count()
    late_count = Attendance.objects.filter(date=today, status="LATE").count()

    # Department Distribution
    department_data = Department.objects.annotate(
        total=Count('employee')
    )

    # Employee List
    employees = Employee.objects.select_related('user', 'department')
   

    # Leave Requests (latest)
    leave_requests = LeaveRequest.objects.filter(status="PENDING").order_by('-created_at')[:5]

    context = {
        "present_count": present_count,
        "leave_count": leave_count,
        "late_count": late_count,
        "departments": department_data,
        "employees": employees,
        "leave_requests": leave_requests,
    }

    for i in context:
        print(context[i])
    return render(request, "hrmanagement.html", context)


