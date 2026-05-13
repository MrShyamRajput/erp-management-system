# views.py

from django.shortcuts import render
from django.db.models import Sum, Count, Avg
from django.db.models.functions import ExtractMonth
from django.utils import timezone

# Finance
from finance.models import Invoice

# HR
from hr.models import (
    Employee,
    Attendance,
    LeaveRequest,
    Department
)

# Inventory
from inventory.models import (
    Product,
    Warehouse,
    InventoryStocks
)

# Procurement
from procurement.models import (
    Supplier,
    PurchaseOrder
)

# Sales
from sales.models import Order


def dashboard(request):

    today = timezone.now()

    # =====================================================
    # FINANCE
    # =====================================================

    paid_invoices = Invoice.objects.filter(status='paid')

    total_revenue = paid_invoices.aggregate(
        total=Sum('amount')
    )['total'] or 0

    this_month_revenue = paid_invoices.filter(
        created_at__month=today.month
    ).aggregate(
        total=Sum('amount')
    )['total'] or 0

    avg_monthly_revenue = paid_invoices.aggregate(
        avg=Avg('amount')
    )['avg'] or 0

    overdue_invoices = Invoice.objects.filter(
        status='overdue'
    ).count()

    recent_invoices = Invoice.objects.order_by(
        '-created_at'
    )[:8]

    activity_invoices = Invoice.objects.order_by(
        '-created_at'
    )[:4]

    # =====================================================
    # SALES
    # =====================================================

    total_orders = Order.objects.count()

    active_orders = Order.objects.filter(
        status__in=['pending', 'shipped']
    ).count()

    pending_orders = Order.objects.filter(
        status='pending'
    ).count()

    shipped_orders = Order.objects.filter(
        status='shipped'
    ).count()

    delivered_orders = Order.objects.filter(
        status='delivered'
    ).count()

    recent_orders = Order.objects.order_by(
        '-created_at'
    )[:8]

    activity_orders = Order.objects.order_by(
        '-created_at'
    )[:4]

    # =====================================================
    # HR
    # =====================================================

    total_employees = Employee.objects.count()

    active_employees = Employee.objects.filter(
        status='ACTIVE'
    ).count()

    dept_count = Department.objects.count()

    present_today = Attendance.objects.filter(
        date=today.date(),
        status='PRESENT'
    ).count()

    pending_leave_requests = LeaveRequest.objects.filter(
        status='PENDING'
    ).select_related('employee')[:5]

    leave_pending = pending_leave_requests.count()

    # =====================================================
    # INVENTORY
    # =====================================================

    total_stock = InventoryStocks.objects.aggregate(
        total=Sum('quantity')
    )['total'] or 0

    warehouse_count = Warehouse.objects.count()

    low_stock_items = InventoryStocks.objects.filter(
        quantity__lt=10
    ).select_related(
        'product',
        'warehouse'
    )[:5]

    low_stock_count = low_stock_items.count()

    # =====================================================
    # PROCUREMENT
    # =====================================================

    total_suppliers = Supplier.objects.count()

    total_purchase_orders = PurchaseOrder.objects.count()

    po_status_queryset = PurchaseOrder.objects.values(
        'status'
    ).annotate(
        total=Count('id')
    )

    po_status_labels = []
    po_status_data = []

    for item in po_status_queryset:

        po_status_labels.append(item['status'])
        po_status_data.append(item['total'])

    # =====================================================
    # REVENUE CHART
    # =====================================================

    revenue_chart_queryset = paid_invoices.annotate(
        month=ExtractMonth('created_at')
    ).values(
        'month'
    ).annotate(
        total=Sum('amount')
    ).order_by('month')

    revenue_by_month = [0] * 12

    for item in revenue_chart_queryset:

        revenue_by_month[item['month'] - 1] = float(
            item['total']
        )

    # =====================================================
    # ORDER CHART
    # =====================================================

    order_chart_queryset = Order.objects.annotate(
        month=ExtractMonth('created_at')
    ).values(
        'month'
    ).annotate(
        total=Count('id')
    ).order_by('month')

    orders_by_month = [0] * 12

    for item in order_chart_queryset:

        orders_by_month[item['month'] - 1] = item['total']

    # =====================================================
    # MONTH LABELS
    # =====================================================

    month_labels = [
        "Jan",
        "Feb",
        "Mar",
        "Apr",
        "May",
        "Jun",
        "Jul",
        "Aug",
        "Sep",
        "Oct",
        "Nov",
        "Dec"
    ]

    # =====================================================
    # BEST MONTH
    # =====================================================

    best_month = "—"

    if max(revenue_by_month) > 0:

        best_month_index = revenue_by_month.index(
            max(revenue_by_month)
        )

        best_month = month_labels[best_month_index]

    # =====================================================
    # REVENUE GROWTH
    # =====================================================

    revenue_growth = 0

    if len(revenue_by_month) >= 2:

        current_month = revenue_by_month[today.month - 1]

        previous_month = revenue_by_month[today.month - 2]

        if previous_month > 0:

            revenue_growth = round(
                (
                    (current_month - previous_month)
                    / previous_month
                ) * 100,
                1
            )

    # =====================================================
    # HEALTH SCORE
    # =====================================================

    health_score = 85

    if low_stock_count > 5:
        health_score -= 10

    if overdue_invoices > 5:
        health_score -= 10

    if delivered_orders > pending_orders:
        health_score += 5

    health_score = min(max(health_score, 0), 100)

    # =====================================================
    # CONTEXT
    # =====================================================

    context = {

        # Date
        'today': today,

        # Revenue
        'total_revenue': total_revenue,
        'this_month_revenue': this_month_revenue,
        'avg_monthly_revenue': avg_monthly_revenue,
        'revenue_growth': revenue_growth,

        # Orders
        'total_orders': total_orders,
        'active_orders': active_orders,
        'pending_orders': pending_orders,
        'shipped_orders': shipped_orders,
        'delivered_orders': delivered_orders,

        # Employees
        'total_employees': total_employees,
        'active_employees': active_employees,
        'dept_count': dept_count,

        # Inventory
        'total_stock': total_stock,
        'warehouse_count': warehouse_count,
        'low_stock_items': low_stock_items,
        'low_stock_count': low_stock_count,

        # Finance
        'overdue_invoices': overdue_invoices,
        'recent_invoices': recent_invoices,

        # Procurement
        'total_purchase_orders': total_purchase_orders,
        'total_suppliers': total_suppliers,
        'po_status_labels': po_status_labels,
        'po_status_data': po_status_data,

        # Attendance
        'present_today': present_today,

        # Leaves
        'pending_leave_requests': pending_leave_requests,
        'leave_pending': leave_pending,

        # Orders Table
        'recent_orders': recent_orders,

        # Activity
        'activity_invoices': activity_invoices,
        'activity_orders': activity_orders,

        # Charts
        'revenue_by_month': revenue_by_month,
        'orders_by_month': orders_by_month,
        'month_labels': month_labels,

        # Other
        'best_month': best_month,
        'health_score': health_score,
    }

    return render(
        request,
        'dashboard.html',
        context
    )