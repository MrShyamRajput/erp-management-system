from django.contrib import admin
from django.urls import path,include
from .views import landing_page
from user.views import userManagement,hrManagement


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',landing_page,name="landing_page" ),


    path("auth/",include("auth.urls")),
    
    path("dashboard/",include("dashboard.urls")),
    
    path("inventory/",include("inventory.urls")),

    path('usermanagement/',userManagement,name="userManagement" ),
    path('hrmanagement/',hrManagement,name="hrmanagement" ),
]
