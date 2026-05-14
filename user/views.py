from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.core.paginator import Paginator
from django.db.models import Q
from .models import User


def userManagement(request):
    users_qs = User.objects.all().order_by("-date_joined")

    query = request.GET.get("q", "").strip()
    role  = request.GET.get("role", "").strip()

    if query:
        users_qs = users_qs.filter(
            Q(username__icontains=query) |
            Q(email__icontains=query)    |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query)  |
            Q(role__icontains=query)
        )

    if role:
        users_qs = users_qs.filter(role=role)

    # --- counts (always from full DB, not filtered) ---
    total_users    = User.objects.count()
    employee_count = User.objects.filter(role="employee").count()
    admin_count    = User.objects.filter(role="admin").count()
    manager_count  = User.objects.filter(role="manager").count()
    hr_count       = User.objects.filter(role="hr").count()
    active_count   = User.objects.filter(is_active=True).count()

    # --- pagination ---
    paginator   = Paginator(users_qs, 10)
    page_number = request.GET.get("page", 1)
    page_obj    = paginator.get_page(page_number)

    context = {
        "users":         page_obj,
        "page_obj":      page_obj,
        "total_users":   total_users,
        "employee_count": employee_count,
        "admin_count":   admin_count,
        "manager_count": manager_count,
        "hr_count":      hr_count,
        "active_count":  active_count,
        "show_modal":    False,
    }
    return render(request, "usermanagement.html", context)


def createUser(request):
    if request.method != "POST":
        return redirect("userManagement")

    username      = request.POST.get("username", "").strip()
    email         = request.POST.get("email", "").strip()
    first_name    = request.POST.get("first_name", "").strip()
    last_name     = request.POST.get("last_name", "").strip()
    password      = request.POST.get("password", "")
    phone         = request.POST.get("phone", "").strip()
    role          = request.POST.get("role", "")
    is_active     = request.POST.get("is_active") == "on"
    profile_image = request.FILES.get("profile_image")

    # --- validation ---
    if not username:
        messages.error(request, "Username is required.")
        return render(request, "usermanagement.html", _base_context(show_modal=True))

    if User.objects.filter(username=username).exists():
        messages.error(request, f"Username '{username}' is already taken.")
        return render(request, "usermanagement.html", _base_context(show_modal=True))

    if email and User.objects.filter(email=email).exists():
        messages.error(request, "A user with that email already exists.")
        return render(request, "usermanagement.html", _base_context(show_modal=True))

    if not password:
        messages.error(request, "Password is required.")
        return render(request, "usermanagement.html", _base_context(show_modal=True))

    # --- create ---
    user = User(
        username=username,
        email=email,
        first_name=first_name,
        last_name=last_name,
        phone=phone,
        role=role,
        is_active=is_active,
        password=make_password(password),
    )
    if profile_image:
        user.profile_image = profile_image

    user.save()
    messages.success(request, f"User '{username}' created successfully.")
    return redirect("userManagement")


def _base_context(show_modal=False):
    """Helper to rebuild stats context when re-rendering after a form error."""
    return {
        "users":          User.objects.all().order_by("-date_joined")[:10],
        "total_users":    User.objects.count(),
        "employee_count": User.objects.filter(role="employee").count(),
        "admin_count":    User.objects.filter(role="admin").count(),
        "manager_count":  User.objects.filter(role="manager").count(),
        "hr_count":       User.objects.filter(role="hr").count(),
        "active_count":   User.objects.filter(is_active=True).count(),
        "show_modal":     show_modal,
    }