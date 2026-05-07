from django.urls import path
from user.views import userManagement


urlpatterns = [
    path('',userManagement,name="userManagement" ),
]