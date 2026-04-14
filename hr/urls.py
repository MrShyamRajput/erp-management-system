from django.urls import path
from .views import hrmanagement
urlpatterns= [
    path('', views.hrmanagement, name='hrmanagement'),
    
]