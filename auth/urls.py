from django.urls import path
from .views import login_page,create_user
urlpatterns=[
    path("login/",login_page,name="loginpage"),
    path("create_user/",create_user,name="create_user"),
    
]