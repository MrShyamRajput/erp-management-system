from django.shortcuts import render, get_object_or_404, redirect
from django.utils.timezone import now
from django.db.models import Count, Q
from django.contrib import messages

from .models import Employee, Attendance, LeaveRequest, Department
from django.contrib.auth import get_user_model

User = get_user_model()


def hr_dashboard(request):
    today = now().date()

    employees = Employee.objects.select_related('user', 'department').order_by(
        'user__first_name', 'user__last_name'
    )

    total_employees = employees.count()

    # Attendance counts for today
    present_count = Attendance.objects.filter(date=today, status="PRESENT").count()
    late_count    = Attendance.objects.filter(date=today, status="LATE").count()

    marked_today  = Attendance.objects.filter(date=today).values_list('employee_id', flat=True)
    absent_count  = employees.exclude(id__in=marked_today).count()

    # On-leave today (approved leaves covering today)
    leave_count = LeaveRequest.objects.filter(
        status="APPROVED",
        start_date__lte=today,
        end_date__gte=today
    ).count()

    # Department distribution
    departments = Department.objects.annotate(total=Count('employee'))

    # Leave requests — filter by status tab
    status_filter = request.GET.get('leave_status', 'PENDING')
    leave_requests = LeaveRequest.objects.select_related(
        'employee__user', 'employee__department'
    ).order_by('-created_at')

    if status_filter in ('PENDING', 'APPROVED', 'REJECTED'):
        leave_requests = leave_requests.filter(status=status_filter)

    leave_requests = leave_requests[:10]

    # Counts per status for badge
    pending_count  = LeaveRequest.objects.filter(status='PENDING').count()
    approved_count = LeaveRequest.objects.filter(status='APPROVED').count()
    rejected_count = LeaveRequest.objects.filter(status='REJECTED').count()

    # Search / filter employees
    q    = request.GET.get('q', '').strip()
    dept = request.GET.get('dept', '').strip()
    emp_status = request.GET.get('emp_status', '').strip()

    if q:
        employees = employees.filter(
            Q(user__first_name__icontains=q) |
            Q(user__last_name__icontains=q)  |
            Q(user__email__icontains=q)
        )
    if dept:
        employees = employees.filter(department_id=dept)
    if emp_status:
        employees = employees.filter(status=emp_status)

    context = {
        "today":          today,
        "present_count":  present_count,
        "absent_count":   absent_count,
        "late_count":     late_count,
        "leave_count":    leave_count,
        "total_employees": total_employees,
        "employees":      employees,
        "departments":    departments,
        "leave_requests": leave_requests,
        "leave_status":   status_filter,
        "pending_count":  pending_count,
        "approved_count": approved_count,
        "rejected_count": rejected_count,
        # for department dropdown
        "all_departments": Department.objects.all(),
        # users who don't yet have an Employee record (for Add Employee modal)
        "eligible_users": User.objects.exclude(
            id__in=Employee.objects.values_list('user_id', flat=True)
        ).order_by('first_name', 'last_name'),
        # all active employees (for Leave Request modal)
        "all_employees": Employee.objects.select_related('user').filter(
            status='ACTIVE'
        ).order_by('user__first_name', 'user__last_name'),
        # re-open modals on validation error
        "show_emp_modal":   False,
        "show_leave_modal": False,
    }
    return render(request, "hrmanagement.html", context)


def update_leave(request, pk):
    """Approve or Reject a leave request via POST."""
    if request.method != 'POST':
        return redirect('hr_dashboard')

    leave = get_object_or_404(LeaveRequest, pk=pk)
    action = request.POST.get('action')

    if action == 'approve':
        leave.status = 'APPROVED'
        leave.save()
        messages.success(request, f"Leave for {leave.employee.user.get_full_name()} approved.")
    elif action == 'reject':
        leave.status = 'REJECTED'
        leave.save()
        messages.error(request, f"Leave for {leave.employee.user.get_full_name()} rejected.")

    return redirect(f"{request.META.get('HTTP_REFERER', '/hr/')}#leave-requests")


def create_employee(request):
    if request.method != 'POST':
        return redirect('hr_dashboard')

    user_id    = request.POST.get('user_id')
    dept_id    = request.POST.get('department')
    status     = request.POST.get('status', 'ACTIVE')

    if not user_id:
        messages.error(request, "Please select a user.")
        return redirect('hr_dashboard')

    user = get_object_or_404(User, pk=user_id)

    if Employee.objects.filter(user=user).exists():
        messages.error(request, f"{user.get_full_name() or user.username} already has an Employee record.")
        return redirect('hr_dashboard')

    department = None
    if dept_id:
        from .models import Department as Dept
        department = Dept.objects.filter(pk=dept_id).first()

    Employee.objects.create(user=user, department=department, status=status)
    messages.success(request, f"Employee '{user.get_full_name() or user.username}' added successfully.")
    return redirect('hr_dashboard')


def create_leave_request(request):
    if request.method != 'POST':
        return redirect('hr_dashboard')

    emp_id     = request.POST.get('employee_id')
    leave_type = request.POST.get('leave_type')
    start_date = request.POST.get('start_date')
    end_date   = request.POST.get('end_date')
    reason     = request.POST.get('reason', '').strip()

    if not all([emp_id, leave_type, start_date, end_date]):
        messages.error(request, "All fields are required for a leave request.")
        return redirect('hr_dashboard')

    employee = get_object_or_404(Employee, pk=emp_id)

    if start_date > end_date:
        messages.error(request, "Start date cannot be after end date.")
        return redirect('hr_dashboard')

    LeaveRequest.objects.create(
        employee=employee,
        leave_type=leave_type,
        start_date=start_date,
        end_date=end_date,
        reason=reason,
        status='PENDING',
    )
    messages.success(request, f"Leave request for {employee.user.get_full_name() or employee.user.username} submitted.")
    return redirect('hr_dashboard')