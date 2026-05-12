# finance/urls.py

from django.urls import path
from .views import finance_dashboard,create_invoice

urlpatterns = [

    path(
        '',
        finance_dashboard,
        name='finance_dashboard'
    ),

    path(
        'create-invoice/',
        create_invoice,
        name='create_invoice'
    ),

]