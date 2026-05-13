# reports/views.py

import json
from django.shortcuts import render, redirect
from django.db.models import Sum, Count, Q
from django.utils import timezone
from datetime import timedelta, date
from collections import defaultdict
from django.http import HttpResponse

# Import all models
from finance.models import Invoice
from hr.models import Employee, Department, Attendance, LeaveRequest
from inventory.models import (
    InventoryStocks, StockTransaction, Product, Warehouse, Category
)
from procurement.models import Supplier, PurchaseOrder
from sales.models import Order
from reports.models import ReportLog


def reports_dashboard(request):
    """
    Main reports & analytics dashboard view.
    Supports ?range=7|30|90 to filter by date range.
    """

    # ── Date Range ──────────────────────────────────────────
    range_days = int(request.GET.get('range', 30))
    today = date.today()
    start_date = today - timedelta(days=range_days)
    prev_start = start_date - timedelta(days=range_days)  # for comparison

    # ═══════════════════════════════════════════════════════
    #  KPI — OVERVIEW
    # ═══════════════════════════════════════════════════════

    # Revenue (from paid invoices)
    total_revenue = Invoice.objects.filter(
        status='paid', created_at__date__gte=start_date
    ).aggregate(s=Sum('amount'))['s'] or 0

    prev_revenue = Invoice.objects.filter(
        status='paid',
        created_at__date__gte=prev_start,
        created_at__date__lt=start_date
    ).aggregate(s=Sum('amount'))['s'] or 0

    if prev_revenue > 0:
        revenue_growth = round(((total_revenue - prev_revenue) / prev_revenue) * 100, 1)
    elif total_revenue > 0:
        revenue_growth = 100
    else:
        revenue_growth = 0

    # Orders
    orders_qs = Order.objects.filter(created_at__date__gte=start_date)
    total_orders     = orders_qs.count()
    pending_orders   = orders_qs.filter(status='pending').count()
    shipped_orders   = orders_qs.filter(status='shipped').count()
    delivered_orders = orders_qs.filter(status='delivered').count()

    # Invoices
    invoices_qs   = Invoice.objects.filter(created_at__date__gte=start_date)
    total_invoices   = invoices_qs.count()
    paid_invoices    = invoices_qs.filter(status='paid').count()
    pending_invoices = invoices_qs.filter(status='pending').count()
    overdue_invoices = invoices_qs.filter(status='overdue').count()

    paid_amount    = invoices_qs.filter(status='paid').aggregate(s=Sum('amount'))['s'] or 0
    pending_amount = invoices_qs.filter(status='pending').aggregate(s=Sum('amount'))['s'] or 0
    overdue_amount = invoices_qs.filter(status='overdue').aggregate(s=Sum('amount'))['s'] or 0
    collection_rate = round((paid_invoices / total_invoices * 100), 1) if total_invoices else 0

    # Inventory KPIs
    total_stock_items = InventoryStocks.objects.aggregate(s=Sum('quantity'))['s'] or 0
    warehouse_count   = Warehouse.objects.count()

    # ─────────────────────────────────────────────────────
    # CHART DATA — Revenue & Orders by Month
    # ─────────────────────────────────────────────────────
    month_labels, revenue_by_month, orders_by_month = [], [], []
    for i in range(11, -1, -1):
        d = today.replace(day=1) - timedelta(days=i * 30)
        label = d.strftime('%b')
        month_start = d.replace(day=1)
        # next month start
        if month_start.month == 12:
            month_end = month_start.replace(year=month_start.year + 1, month=1)
        else:
            month_end = month_start.replace(month=month_start.month + 1)

        rev = Invoice.objects.filter(
            status='paid',
            created_at__date__gte=month_start,
            created_at__date__lt=month_end
        ).aggregate(s=Sum('amount'))['s'] or 0

        ord_count = Order.objects.filter(
            created_at__date__gte=month_start,
            created_at__date__lt=month_end
        ).count()

        month_labels.append(label)
        revenue_by_month.append(float(rev))
        orders_by_month.append(ord_count)

    # Order Status chart data
    order_status_labels = ['Pending', 'Shipped', 'Delivered']
    order_status_data   = [
        Order.objects.filter(status='pending').count(),
        Order.objects.filter(status='shipped').count(),
        Order.objects.filter(status='delivered').count(),
    ]

    # Supplier performance chart
    supplier_perf_labels = ['Excellent', 'Good', 'Average']
    supplier_perf_data   = [
        Supplier.objects.filter(performance='excellent').count(),
        Supplier.objects.filter(performance='good').count(),
        Supplier.objects.filter(performance='average').count(),
    ]

    # Invoice status chart (Finance tab)
    invoice_status_labels = ['Paid', 'Pending', 'Overdue']
    invoice_status_data   = [
        Invoice.objects.filter(status='paid').count(),
        Invoice.objects.filter(status='pending').count(),
        Invoice.objects.filter(status='overdue').count(),
    ]

    # ─────────────────────────────────────────────────────
    # WAREHOUSE UTILIZATION
    # ─────────────────────────────────────────────────────
    warehouse_utilization = []
    for wh in Warehouse.objects.all():
        used = InventoryStocks.objects.filter(warehouse=wh).aggregate(s=Sum('quantity'))['s'] or 0
        cap  = wh.capacity or 1
        warehouse_utilization.append({
            'name':     wh.name,
            'used':     used,
            'capacity': cap,
            'pct':      min(round((used / cap) * 100), 100),
        })

    # ─────────────────────────────────────────────────────
    # HR DATA
    # ─────────────────────────────────────────────────────
    total_employees  = Employee.objects.count()
    active_employees = Employee.objects.filter(status='ACTIVE').count()
    leave_pending    = LeaveRequest.objects.filter(status='PENDING').count()

    today_att = Attendance.objects.filter(date=today)
    present_today = today_att.filter(status='PRESENT').count()
    absent_today  = today_att.filter(status='ABSENT').count()
    late_today    = today_att.filter(status='LATE').count()
    hr_attendance_data = [present_today, absent_today, late_today]

    # Dept distribution
    dept_qs = (
        Department.objects
        .annotate(emp_count=Count('employee'))
        .values('name', 'emp_count')
        .order_by('-emp_count')
    )
    dept_labels = [d['name'] for d in dept_qs]
    dept_data   = [d['emp_count'] for d in dept_qs]

    # Leave status
    leave_status_labels = ['Pending', 'Approved', 'Rejected']
    leave_status_data   = [
        LeaveRequest.objects.filter(status='PENDING').count(),
        LeaveRequest.objects.filter(status='APPROVED').count(),
        LeaveRequest.objects.filter(status='REJECTED').count(),
    ]

    # ─────────────────────────────────────────────────────
    # INVENTORY CHARTS
    # ─────────────────────────────────────────────────────
    cat_qs = (
        InventoryStocks.objects
        .values('product__category__name')
        .annotate(total=Sum('quantity'))
        .order_by('-total')
    )
    stock_category_labels = [c['product__category__name'] or 'Uncategorized' for c in cat_qs]
    stock_category_data   = [c['total'] for c in cat_qs]

    # Stock In/Out by last 8 weeks (weekly)
    stock_txn_labels, stock_txn_in, stock_txn_out = [], [], []
    for i in range(7, -1, -1):
        wk_start = today - timedelta(days=i * 7 + 7)
        wk_end   = today - timedelta(days=i * 7)
        label = wk_start.strftime('%b %d')
        ins  = StockTransaction.objects.filter(
            transaction_type='IN',
            created_at__date__gte=wk_start,
            created_at__date__lt=wk_end
        ).aggregate(s=Sum('quantity'))['s'] or 0
        outs = StockTransaction.objects.filter(
            transaction_type='OUT',
            created_at__date__gte=wk_start,
            created_at__date__lt=wk_end
        ).aggregate(s=Sum('quantity'))['s'] or 0
        stock_txn_labels.append(label)
        stock_txn_in.append(ins)
        stock_txn_out.append(outs)

    # ─────────────────────────────────────────────────────
    # PROCUREMENT CHARTS
    # ─────────────────────────────────────────────────────
    po_status_raw = (
        PurchaseOrder.objects
        .values('status')
        .annotate(cnt=Count('id'))
    )
    po_status_labels = [p['status'].replace('_', ' ').title() for p in po_status_raw]
    po_status_data   = [p['cnt'] for p in po_status_raw]

    supplier_seg_raw = (
        Supplier.objects
        .values('segment')
        .annotate(cnt=Count('id'))
    )
    supplier_seg_labels = [s['segment'].replace('_', ' ').title() for s in supplier_seg_raw]
    supplier_seg_data   = [s['cnt'] for s in supplier_seg_raw]

    # ─────────────────────────────────────────────────────
    # TOP PRODUCTS (Sales)
    # ─────────────────────────────────────────────────────
    top_raw = (
        Order.objects
        .values('product')
        .annotate(qty=Sum('quantity'))
        .order_by('-qty')[:8]
    )
    max_qty = top_raw[0]['qty'] if top_raw else 1
    top_products = [
        {'product': p['product'], 'qty': p['qty'], 'pct': round(p['qty'] / max_qty * 100)}
        for p in top_raw
    ]

    # ─────────────────────────────────────────────────────
    # TABLE QUERYSETS
    # ─────────────────────────────────────────────────────
    recent_invoices = Invoice.objects.order_by('-created_at')[:8]
    all_invoices    = Invoice.objects.order_by('-created_at')[:100]
    recent_orders   = Order.objects.order_by('-created_at')[:8]
    all_orders      = Order.objects.order_by('-created_at')[:100]
    inventory_items = InventoryStocks.objects.select_related(
        'product', 'product__category', 'warehouse'
    ).order_by('-updated_at')[:80]
    leave_requests  = LeaveRequest.objects.select_related('employee').order_by('-created_at')[:30]
    purchase_orders = PurchaseOrder.objects.select_related('supplier').order_by('-created_at')[:50]

    # ─────────────────────────────────────────────────────
    # CONTEXT
    # ─────────────────────────────────────────────────────
    context = {
        # KPIs
        'total_revenue':    total_revenue,
        'revenue_growth':   revenue_growth,
        'total_orders':     total_orders,
        'pending_orders':   pending_orders,
        'shipped_orders':   shipped_orders,
        'delivered_orders': delivered_orders,
        'total_invoices':   total_invoices,
        'paid_invoices':    paid_invoices,
        'pending_invoices': pending_invoices,
        'overdue_invoices': overdue_invoices,
        'paid_amount':      paid_amount,
        'pending_amount':   pending_amount,
        'overdue_amount':   overdue_amount,
        'collection_rate':  collection_rate,
        'total_stock_items': total_stock_items,
        'warehouse_count':  warehouse_count,

        # HR
        'total_employees':   total_employees,
        'active_employees':  active_employees,
        'leave_pending':     leave_pending,
        'present_today':     present_today,
        'absent_today':      absent_today,
        'late_today':        late_today,
        'hr_attendance_data': json.dumps(hr_attendance_data),

        # Warehouse
        'warehouse_utilization': warehouse_utilization,

        # Chart JSON
        'revenue_by_month_labels': json.dumps(month_labels),
        'revenue_by_month_data':   json.dumps(revenue_by_month),
        'orders_by_month_data':    json.dumps(orders_by_month),
        'order_status_labels':     json.dumps(order_status_labels),
        'order_status_data':       json.dumps(order_status_data),
        'supplier_perf_labels':    json.dumps(supplier_perf_labels),
        'supplier_perf_data':      json.dumps(supplier_perf_data),
        'invoice_status_labels':   json.dumps(invoice_status_labels),
        'invoice_status_data':     json.dumps(invoice_status_data),
        'stock_category_labels':   json.dumps(stock_category_labels),
        'stock_category_data':     json.dumps(stock_category_data),
        'stock_txn_labels':        json.dumps(stock_txn_labels),
        'stock_txn_in':            json.dumps(stock_txn_in),
        'stock_txn_out':           json.dumps(stock_txn_out),
        'dept_labels':             json.dumps(dept_labels),
        'dept_data':               json.dumps(dept_data),
        'leave_status_labels':     json.dumps(leave_status_labels),
        'leave_status_data':       json.dumps(leave_status_data),
        'po_status_labels':        json.dumps(po_status_labels),
        'po_status_data':          json.dumps(po_status_data),
        'supplier_seg_labels':     json.dumps(supplier_seg_labels),
        'supplier_seg_data':       json.dumps(supplier_seg_data),

        # Tables
        'recent_invoices':  recent_invoices,
        'all_invoices':     all_invoices,
        'recent_orders':    recent_orders,
        'all_orders':       all_orders,
        'inventory_items':  inventory_items,
        'leave_requests':   leave_requests,
        'purchase_orders':  purchase_orders,
        'top_products':     top_products,
    }

    return render(request, 'reports.html', context)


def create_report(request):
    """Handle the 'New Report' modal form submission."""
    if request.method == 'POST':
        title       = request.POST.get('title', '').strip()
        report_type = request.POST.get('report_type', 'finance')
        if title:
            ReportLog.objects.create(title=title, report_type=report_type)
    return redirect('reports:dashboard')




def export_csv(request):
    return HttpResponse("CSV export coming soon")

def export_pdf(request):
    return HttpResponse("PDF export coming soon")