from django.shortcuts import render
from django.db.models import Sum
from .models import Product,Category, Brand,InventoryStocks,Warehouse
from django.http import JsonResponse
from django.shortcuts import redirect
from django.http import HttpResponse
import json




LOW_STOCK_THRESHOLD=50

def inventory_view(request):
    # Filters
    category_id = request.GET.get('category')
    brand_id = request.GET.get('brand')
    stock_status = request.GET.get('stock')

    # Products with stock
    products = Product.objects.all().select_related('category', 'brand') \
        .annotate(total_stock=Sum('inventorystocks__quantity'))

    # Apply filters
    if category_id:
        products = products.filter(category_id=category_id)

    if brand_id:
        products = products.filter(brand_id=brand_id)

    if stock_status == 'low':
        products = products.filter(total_stock__lt=LOW_STOCK_THRESHOLD)

    elif stock_status == 'out':
        products = products.filter(total_stock__lte=0)

    # Low stock count
    low_stock_count = products.filter(total_stock__lt=LOW_STOCK_THRESHOLD).count()

    # Warehouse data
    warehouses = Warehouse.objects.all()

    # Dropdown data
    categories = Category.objects.all()
    brands = Brand.objects.all()

    context = {
        "products": products,
        "categories": categories,
        "brands": brands,
        "warehouses": warehouses,
        "low_stock_count": low_stock_count,
        "orders_count": 24,  # static for now
    }

    return render(request, "inventry.html", context)
    

def add_category(request):
    if request.method == "POST":
        try:
            name = request.POST.get("name")
            description = request.POST.get("description")

            if not name:
                return JsonResponse({"success": False, "error": "Name required"})

            category = Category.objects.create(
                name=name,
                description=description
            )

            return JsonResponse({
                "success": True,
                "id": category.id,
                "name": category.name
            })

        except Exception as e:
            return JsonResponse({
                "success": False,
                "error": str(e)
            })

    return JsonResponse({"success": False})
def add_brand(request):
    if request.method == "POST":
        name = request.POST.get("name")
        logo = request.FILES.get("logo")

        if not name:
            return JsonResponse({"success": False, "error": "Name required"})

        brand = Brand.objects.create(
            name=name,
            logo=logo
        )

        return JsonResponse({
            "success": True,
            "id": brand.id,
            "name": brand.name
        })

    return JsonResponse({"success": False, "error": "Invalid request"})


def add_product(request):
    if request.method == "POST":
        try:
            name = request.POST.get("name")
            sku = request.POST.get("sku")
            category_id = request.POST.get("category")
            brand_id = request.POST.get("brand")
            price = request.POST.get("price")
            description = request.POST.get("description")
            image = request.FILES.get("image")

            # ✅ Validation
            if not all([name, sku, category_id, brand_id, price]):
                return HttpResponse("Missing required fields")

            # ✅ Get FK objects
            category = Category.objects.get(id=category_id)
            brand = Brand.objects.get(id=brand_id)

            # ✅ Create Product
            product = Product.objects.create(
                name=name,
                sku=sku,
                category=category,
                brand=brand,
                price=price,
                description=description,
                image=image
            )

            return JsonResponse({"success": True})  # ✅ IMPORTAN

        except Exception as e:
            return HttpResponse(f"Error: {str(e)}")

    return HttpResponse("Invalid Request")