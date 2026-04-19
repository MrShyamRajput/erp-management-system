from django.contrib import admin
from django.urls import path,include
from .views import landing_page
from user.views import userManagement,hrManagement
from django.conf import settings
from django.conf.urls.static import static




urlpatterns = [
    path('admin/', admin.site.urls),
    path('',landing_page,name="landing_page" ),


    path("auth/",include("auth.urls")),
    
    path("dashboard/",include("dashboard.urls")),
    
    path("inventory/",include("inventory.urls")),

    path('usermanagement/',userManagement,name="userManagement"),
    path('hrmanagement/',hrManagement,name="hrmanagement"),
    path('hr/', include('hr.urls')),
    path('sales/', include('sales.urls'))
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)