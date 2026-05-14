from django.urls import path
from user.views import userManagement, createUser

urlpatterns = [
    path('', userManagement, name="userManagement"),
    path('create/', createUser,     name="createUser"),
]