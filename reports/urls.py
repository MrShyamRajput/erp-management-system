# reports/urls.py
from django.urls import path
from . import views

app_name = 'reports'  # ← this is the key line

urlpatterns = [
    path('', views.reports_dashboard, name='dashboard'),
    path('create/', views.create_report, name='create'),
    path('export/csv/', views.export_csv, name='export_csv'),
    path('export/pdf/', views.export_pdf, name='export_pdf'),
]