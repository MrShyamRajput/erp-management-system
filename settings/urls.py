from django.urls import path
from . import views

app_name = "settings_app"

urlpatterns = [
    # Main settings page (GET)
    path("", views.settings_view, name="settings"),

    # POST handlers
    path("company/save/",          views.save_company,        name="save_company"),
    path("departments/add/",       views.add_department,      name="add_department"),
    path("departments/<int:dept_id>/delete/", views.delete_department, name="delete_department"),
    path("leave/save/",            views.save_leave_policy,   name="save_leave_policy"),
    path("working-days/save/",     views.save_working_days,   name="save_working_days"),
]