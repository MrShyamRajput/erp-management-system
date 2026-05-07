from django.urls import path
from .views import inventory_view,add_category,add_brand,add_product
urlpatterns=[

    path("",inventory_view,name="inventory"),
    path('add-category/', add_category, name='add_category'),
    path('add-brand/', add_brand, name='add_brand'),
    path('add-product/', add_product, name='add_product'),
    
]