from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Sum, F

from .models import Invoice
from .forms import InvoiceForm

from procurement.models import PurchaseOrder
from sales.models import Order


def finance_dashboard(request):

    form = InvoiceForm()

    # CREATE INVOICE
    if request.method == 'POST':

        form = InvoiceForm(request.POST)

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Invoice Created Successfully!"
            )

            return redirect('finance_dashboard')

    # ALL INVOICES
    invoices = Invoice.objects.all().order_by('-created_at')

    # =========================
    # SALES REVENUE
    # =========================

    total_revenue = Order.objects.filter(
        status='delivered'
    ).aggregate(
        total=Sum(
            F('quantity') * F('price')
        )
    )['total'] or 0

    # =========================
    # PROCUREMENT EXPENSES
    # =========================

    total_expenses = PurchaseOrder.objects.aggregate(
        total=Sum('amount')
    )['total'] or 0

    # =========================
    # NET PROFIT
    # =========================

    net_profit = total_revenue - total_expenses

    # =========================
    # PENDING INVOICES
    # =========================

    pending_invoices = Invoice.objects.filter(
        status='pending'
    ).count()

    # =========================
    # CONTEXT
    # =========================

    context = {

        'form': form,

        'invoices': invoices,

        'total_revenue': total_revenue,

        'total_expenses': total_expenses,

        'net_profit': net_profit,

        'pending_invoices': pending_invoices,

    }

    return render(
        request,
        'finance.html',
        context
    )


def create_invoice(request):

    return redirect('finance_dashboard')