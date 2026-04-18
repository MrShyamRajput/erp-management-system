from django.contrib import admin
from.models import Category,Brand,Product,Warehouse,InventoryStocks,StockTransaction
# Register your models here.


admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(Product)
admin.site.register(Warehouse)
admin.site.register(InventoryStocks)
admin.site.register(StockTransaction)