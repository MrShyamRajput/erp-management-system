from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.views.decorators.http import require_POST
from django.db.models import Count

from hr.models import Department, Employee
from finance.models import Invoice
from .models import CompanySettings, LeavePolicy, WorkingDays

User = get_user_model()

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

_DAY_ORDER = ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"]


def _ensure_defaults():
    """Pre-populate WorkingDays (7 rows) and LeavePolicy (2 rows) if missing."""
    defaults_wd = {
        "MON": True, "TUE": True, "WED": True,
        "THU": True, "FRI": True, "SAT": False, "SUN": False,
    }
    for day_code, is_working in defaults_wd.items():
        WorkingDays.objects.get_or_create(
            day=day_code,
            defaults={"is_working": is_working},
        )

    for leave_type in ("SICK", "ANNUAL"):
        LeavePolicy.objects.get_or_create(
            leave_type=leave_type,
            defaults={"days_allowed": 12, "carry_forward": False},
        )


# ---------------------------------------------------------------------------
# Main settings view
# ---------------------------------------------------------------------------

def settings_view(request):
    _ensure_defaults()

    # --- Company Settings (singleton) ---
    company, _ = CompanySettings.objects.get_or_create(pk=1)

    # --- Departments with employee count ---
    departments = (
        Department.objects.annotate(emp_count=Count("employee"))
        .order_by("name")
    )

    # --- Leave policies ---
    leave_policies = {lp.leave_type: lp for lp in LeavePolicy.objects.all()}

    # --- Working days (ordered Mon → Sun) ---
    wd_qs = WorkingDays.objects.all()
    working_days = sorted(wd_qs, key=lambda w: _DAY_ORDER.index(w.day))

    # --- Finance stats ---
    finance_stats = {
        "total": Invoice.objects.count(),
        "paid": Invoice.objects.filter(status="paid").count(),
        "pending": Invoice.objects.filter(status="pending").count(),
        "overdue": Invoice.objects.filter(status="overdue").count(),
    }

    # --- User & access stats ---
    all_users = User.objects.all()
    user_stats = {
        "total": all_users.count(),
        "admin": all_users.filter(role="admin").count(),
        "manager": all_users.filter(role="manager").count(),
        "employee": all_users.filter(role="employee").count(),
        "hr": all_users.filter(role="hr").count(),
        "active": all_users.filter(is_active=True).count(),
        "inactive": all_users.filter(is_active=False).count(),
    }

    context = {
        "company": company,
        "departments": departments,
        "leave_policies": leave_policies,
        "working_days": working_days,
        "finance_stats": finance_stats,
        "user_stats": user_stats,
        # Pass the active section so the sidebar stays highlighted after POST
        "active_section": request.GET.get("section", "company"),
    }
    return render(request, "settings.html", context)


# ---------------------------------------------------------------------------
# POST handlers
# ---------------------------------------------------------------------------

@require_POST
def save_company(request):
    company, _ = CompanySettings.objects.get_or_create(pk=1)
    company.name = request.POST.get("name", "").strip()
    company.address = request.POST.get("address", "").strip()
    company.email = request.POST.get("email", "").strip()
    company.phone = request.POST.get("phone", "").strip()
    company.currency = request.POST.get("currency", "INR").strip()
    company.timezone = request.POST.get("timezone", "Asia/Kolkata").strip()

    fys = request.POST.get("financial_year_start", "").strip()
    company.financial_year_start = fys if fys else None

    if "logo" in request.FILES:
        company.logo = request.FILES["logo"]

    company.save()
    messages.success(request, "Company settings saved successfully.")
    return redirect("/settings/?section=company")


@require_POST
def add_department(request):
    name = request.POST.get("dept_name", "").strip()
    if not name:
        messages.error(request, "Department name cannot be empty.")
    elif Department.objects.filter(name__iexact=name).exists():
        messages.error(request, f'Department "{name}" already exists.')
    else:
        Department.objects.create(name=name)
        messages.success(request, f'Department "{name}" added successfully.')
    return redirect("/settings/?section=departments")


@require_POST
def delete_department(request, dept_id):
    dept = get_object_or_404(Department, pk=dept_id)
    if dept.employee.exists():
        messages.error(
            request,
            f'Cannot delete "{dept.name}" — it has employees assigned to it.',
        )
    else:
        dept_name = dept.name
        dept.delete()
        messages.success(request, f'Department "{dept_name}" deleted.')
    return redirect("/settings/?section=departments")


@require_POST
def save_leave_policy(request):
    for leave_type in ("SICK", "ANNUAL"):
        lp, _ = LeavePolicy.objects.get_or_create(leave_type=leave_type)
        days_key = f"days_{leave_type.lower()}"
        cf_key = f"carry_forward_{leave_type.lower()}"
        try:
            lp.days_allowed = int(request.POST.get(days_key, lp.days_allowed))
        except ValueError:
            pass
        lp.carry_forward = cf_key in request.POST
        lp.save()
    messages.success(request, "Leave policies updated successfully.")
    return redirect("/settings/?section=leave")


@require_POST
def save_working_days(request):
    _ensure_defaults()
    for day_code in _DAY_ORDER:
        wd = WorkingDays.objects.get(day=day_code)
        wd.is_working = f"working_{day_code}" in request.POST
        start = request.POST.get(f"start_{day_code}", "").strip()
        end = request.POST.get(f"end_{day_code}", "").strip()
        if start:
            wd.work_start = start
        if end:
            wd.work_end = end
        wd.save()
    messages.success(request, "Working days & hours updated successfully.")
    return redirect("/settings/?section=working_days")