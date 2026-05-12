from django.shortcuts import render
from django.db.models import Sum, Count, Avg, F, DecimalField, ExpressionWrapper
from django.db.models.functions import TruncMonth
from sales.models import Order
from decimal import Decimal

def reports_dashboard(request):

    # =========================================
    # TOTAL REVENUE
    # =========================================

    total_revenue = Order.objects.aggregate(

        total=Sum(

            ExpressionWrapper(
                F('price') * F('quantity'),
                output_field=DecimalField()
            )

        )

    )['total'] or 0

    # =========================================
    # TOTAL ORDERS
    # =========================================

    total_orders = Order.objects.count()
    print(total_orders,total_revenue,)

    # =========================================
    # DELIVERED ORDERS
    # =========================================

    delivered_orders = Order.objects.filter(
        status='delivered'
    ).count()

    # =========================================
    # PENDING ORDERS
    # =========================================

    pending_orders = Order.objects.filter(
        status='pending'
    ).count()

    # =========================================
    # SHIPPED ORDERS
    # =========================================

    shipped_orders = Order.objects.filter(
        status='shipped'
    ).count()

    # =========================================
    # TOTAL CUSTOMERS
    # =========================================

    total_customers = Order.objects.values(
        'email'
    ).distinct().count()

    # =========================================
    # AVERAGE ORDER VALUE
    # =========================================

    average_order_value = 0

    if total_orders > 0:

        average_order_value = round(
    total_revenue / total_orders,
    2
)

    # =========================================
    # BUSINESS PERFORMANCE INDEX
    # =========================================

    performance_index = 84.2

    # =========================================
    # REVENUE GROWTH %
    # =========================================

    revenue_growth = 12.4

    # =========================================
    # OPERATIONAL EXPENSES
    # =========================================

    operational_expenses = total_revenue * Decimal('0.20')

    # =========================================
    # GROSS MARGIN
    # =========================================

    gross_margin = 32.8

    # =========================================
    # MONTHLY SALES
    # =========================================

    monthly_sales = (

        Order.objects

        .annotate(
            month=TruncMonth('created_at')
        )

        .values('month')

        .annotate(

            total=Sum(

                ExpressionWrapper(
                    F('price') * F('quantity'),
                    output_field=DecimalField()
                )

            )

        )

        .order_by('month')

    )

    # =========================================
    # MAX SALES VALUE
    # =========================================

    max_sales = max(

        [sale['total'] or 0 for sale in monthly_sales],
        default=1

    )

    # =========================================
    # SALES BAR PERCENTAGE
    # =========================================

    for sale in monthly_sales:

        total = sale['total'] or 0

        sale['percent'] = (
            (total / max_sales) * 100
        ) if max_sales else 0

    # =========================================
    # REGION SALES DATA
    # =========================================

    regional_sales = [

        {
            'region': 'North America',
            'amount': 480000,
            'percent': 85,
            'color': 'bg-primary'
        },

        {
            'region': 'European Union',
            'amount': 312000,
            'percent': 62,
            'color': 'bg-tertiary'
        },

        {
            'region': 'Asia-Pacific',
            'amount': 204000,
            'percent': 44,
            'color': 'bg-blue-400'
        },

        {
            'region': 'Latin America',
            'amount': 118000,
            'percent': 28,
            'color': 'bg-indigo-400'
        },

    ]

    # =========================================
    # DIVISION REVENUE
    # =========================================

    division_revenue = [

        {
            'name': 'Enterprise Software',
            'percent': 58,
            'color': 'bg-primary'
        },

        {
            'name': 'Consulting Services',
            'percent': 24,
            'color': 'bg-tertiary'
        },

        {
            'name': 'Hardware Leasing',
            'percent': 18,
            'color': 'bg-gray-400'
        },

    ]

    # =========================================
    # RECENT ORDERS
    # =========================================

    recent_orders = Order.objects.order_by(
        '-created_at'
    )[:5]

    # =========================================
    # CONTEXT
    # =========================================

    context = {

        'total_revenue': total_revenue,

        'total_orders': total_orders,

        'delivered_orders': delivered_orders,

        'pending_orders': pending_orders,

        'shipped_orders': shipped_orders,

        'total_customers': total_customers,

        'average_order_value': average_order_value,

        'performance_index': performance_index,

        'revenue_growth': revenue_growth,

        'operational_expenses': operational_expenses,

        'gross_margin': gross_margin,

        'monthly_sales': monthly_sales,

        'regional_sales': regional_sales,

        'division_revenue': division_revenue,

        'recent_orders': recent_orders,

    }

    return render(

        request,
        'reports.html',
        context

    )