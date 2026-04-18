from django.shortcuts import render
from django.db.models import Sum
from .models import Product,Category, Brand,InventoryStocks,Warehouse
from django.http import JsonResponse
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
    try:
        data = json.loads(request.body.decode('utf-8'))
        name = data.get("name", "").strip()

        # ✅ Validation
        if not name:
            return JsonResponse(
                {"error": "Category name is required"},
                status=400
            )

        # ✅ Duplicate check (case-insensitive)
        if Category.objects.filter(name__iexact=name).exists():
            return JsonResponse(
                {"error": "Category already exists"},
                status=409
            )

        # ✅ Create category
        category = Category.objects.create(name=name)

        # ✅ Success response
        return JsonResponse({
            "id": category.id,
            "name": category.name,
            "message": "Category added successfully"
        }, status=201)

    except json.JSONDecodeError:
        return JsonResponse(
            {"error": "Invalid JSON"},
            status=400
        )

    except Exception as e:
        return JsonResponse(
            {"error": "Something went wrong"},
            status=500
        )