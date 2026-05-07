from django.shortcuts import render
from .models import User
from django.db.models import Q


def userManagement(request):
    users = User.objects.all()

    query = request.GET.get("q")
    role = request.GET.get("role")

    # 🔍 Search
    if query:
        users = users.filter(
            Q(username__icontains=query) |
            Q(email__icontains=query) |
            Q(role__icontains=query)
        )

    # 🎯 Role filter
    if role:
        users = users.filter(role=role)

    # 📊 Counts (filtered ya full? → tum decide karo)
    total_users = users.count()
    employee_count = users.filter(role="employee").count()
    admin_count = users.filter(role="admin").count()
    manager_count = users.filter(role="manager").count()

    context = {
        "users": users,
        "total_users": total_users,
        "employee_count": employee_count,
        "admin_count": admin_count,
        "manager_count": manager_count,
    }

    return render(request, "usermanagement.html", context)

