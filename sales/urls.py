from django.urls import path
from .import views
from .views import create_order

urlpatterns=[
    path('', views.create_order, name='create_order')
]