from django.urls import path
from .views import hr_dashboard, update_leave, create_employee, create_leave_request

urlpatterns = [
    path('',                    hr_dashboard,         name="hr_dashboard"),
    path('leave/<int:pk>/',     update_leave,         name="update_leave"),
    path('employee/create/',    create_employee,      name="create_employee"),
    path('leave/create/',       create_leave_request, name="create_leave_request"),
]