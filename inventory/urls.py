from django.urls import path
from .views import inventory_view,add_category
urlpatterns=[

    path("",inventory_view,name="inventory"),
    path('add-category/', add_category, name='add_category'),
    
]