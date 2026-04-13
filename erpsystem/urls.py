from django.contrib import admin
from django.urls import path,include
from .views import landing_page
from user.views import dashboard,userManagement,hrManagement


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',landing_page,name="landing_page" ),
    path('dashboard/',dashboard,
    name="dashboard_page" ),

    path("auth/",include("auth.urls")),

    path('usermanagement/',userManagement,name="userManagement" ),
    path('hrmanagement/',hrManagement,name="hrmanagement" ),
]
